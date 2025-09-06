from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.crud import report as report_crud
from app.crud import patient as patient_crud
from app.schemas.report import Report, ReportCreate, ReportUpdate, ReportList, ReportStatistics, ReportUpload, AIAnalysisRequest, AIAnalysisResponse
from app.schemas.user import User
import os
import uuid
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=ReportList)
def get_reports(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    patient_id: Optional[int] = Query(None, description="患者ID筛选"),
    report_type: Optional[str] = Query(None, description="报告类型筛选"),
    status: Optional[str] = Query(None, description="状态筛选"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取报告列表"""
    reports = report_crud.get_reports(
        db=db,
        skip=skip,
        limit=limit,
        user_id=current_user.id,
        patient_id=patient_id,
        report_type=report_type,
        status=status,
        search=search
    )
    total = report_crud.get_reports_count(db=db, user_id=current_user.id)
    
    return ReportList(
        reports=reports,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{report_id}", response_model=Report)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取单个报告"""
    report = report_crud.get_report(db, report_id=report_id)
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    # 检查权限：只能查看自己的报告
    if report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限访问此报告")
    
    return report


@router.post("/", response_model=Report)
def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新报告"""
    # 检查报告编号是否已存在
    existing_report = report_crud.get_report_by_report_id(db, report.report_id)
    if existing_report:
        raise HTTPException(status_code=400, detail="报告编号已存在")
    
    # 检查患者是否存在且属于当前用户
    patient = patient_crud.get_patient(db, report.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="患者不存在")
    if patient.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限为此患者创建报告")
    
    return report_crud.create_report(db=db, report=report, user_id=current_user.id)


@router.post("/upload", response_model=Report)
async def upload_report(
    background_tasks: BackgroundTasks,
    patient_id: int = Query(..., description="患者ID"),
    report_type: str = Query(..., description="报告类型"),
    title: str = Query(..., description="报告标题"),
    description: Optional[str] = Query(None, description="报告描述"),
    file: UploadFile = File(..., description="报告文件"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传报告文件"""
    # 检查患者是否存在且属于当前用户
    patient = patient_crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="患者不存在")
    if patient.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限为此患者上传报告")
    
    # 验证文件类型
    allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx'}
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    
    # 验证文件大小 (10MB)
    if file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件大小不能超过10MB")
    
    # 生成唯一文件名
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{file_id}{file_extension}"
    
    # 保存文件
    upload_dir = "uploads/reports"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail="文件保存失败")
    
    # 创建报告记录
    report_data = ReportCreate(
        report_id=f"RPT{datetime.now().strftime('%Y%m%d%H%M%S')}{file_id[:8]}",
        patient_id=patient_id,
        report_type=report_type,
        title=title,
        description=description,
        file_path=file_path,
        file_size=file.size
    )
    
    report = report_crud.create_report(db=db, report=report_data, user_id=current_user.id)
    
    # 后台任务：AI分析
    # background_tasks.add_task(process_report_ai_analysis, report.id)
    
    return report


@router.put("/{report_id}", response_model=Report)
def update_report(
    report_id: int,
    report: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新报告信息"""
    # 检查报告是否存在
    existing_report = report_crud.get_report(db, report_id=report_id)
    if not existing_report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    # 检查权限
    if existing_report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限修改此报告")
    
    # 如果更新报告编号，检查是否与其他报告冲突
    if report.report_id and report.report_id != existing_report.report_id:
        conflict_report = report_crud.get_report_by_report_id(db, report.report_id)
        if conflict_report:
            raise HTTPException(status_code=400, detail="报告编号已存在")
    
    updated_report = report_crud.update_report(db=db, report_id=report_id, report=report)
    if not updated_report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    return updated_report


@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除报告"""
    # 检查报告是否存在
    existing_report = report_crud.get_report(db, report_id=report_id)
    if not existing_report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    # 检查权限
    if existing_report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限删除此报告")
    
    # 删除文件
    if existing_report.file_path and os.path.exists(existing_report.file_path):
        try:
            os.remove(existing_report.file_path)
        except Exception:
            pass  # 忽略文件删除错误
    
    success = report_crud.delete_report(db=db, report_id=report_id)
    if not success:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    return {"message": "报告删除成功"}


@router.get("/patient/{patient_id}", response_model=List[Report])
def get_patient_reports(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取患者的所有报告"""
    # 检查患者是否存在且属于当前用户
    patient = patient_crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="患者不存在")
    if patient.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限访问此患者的报告")
    
    reports = report_crud.get_reports_by_patient(
        db=db, 
        patient_id=patient_id, 
        user_id=current_user.id
    )
    return reports


@router.get("/type/{report_type}", response_model=List[Report])
def get_reports_by_type(
    report_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """根据报告类型获取报告列表"""
    reports = report_crud.get_reports_by_type(
        db=db, 
        report_type=report_type, 
        user_id=current_user.id
    )
    return reports


@router.get("/status/{status}", response_model=List[Report])
def get_reports_by_status(
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """根据状态获取报告列表"""
    reports = report_crud.get_reports_by_status(
        db=db, 
        status=status, 
        user_id=current_user.id
    )
    return reports


@router.get("/statistics/overview", response_model=ReportStatistics)
def get_report_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取报告统计信息"""
    stats = report_crud.get_reports_statistics(db=db, user_id=current_user.id)
    return ReportStatistics(**stats)


@router.post("/{report_id}/ai-analysis", response_model=AIAnalysisResponse)
def request_ai_analysis(
    report_id: int,
    analysis_request: AIAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """请求AI分析报告"""
    # 检查报告是否存在
    report = report_crud.get_report(db, report_id=report_id)
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    # 检查权限
    if report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限分析此报告")
    
    # 检查报告状态
    if report.status.value == "completed":
        raise HTTPException(status_code=400, detail="报告已完成分析")
    
    # 更新报告状态为处理中
    report_crud.update_report_status(db=db, report_id=report_id, status="processing")
    
    # 后台任务：执行AI分析
    # background_tasks.add_task(perform_ai_analysis, report_id, analysis_request.analysis_type)
    
    # 模拟AI分析结果
    ai_analysis = f"基于报告内容的AI分析结果，分析类型：{analysis_request.analysis_type}"
    ai_recommendations = "根据分析结果，建议进行进一步的骨密度检查..."
    
    # 更新AI分析结果
    updated_report = report_crud.update_ai_analysis(
        db=db, 
        report_id=report_id, 
        ai_analysis=ai_analysis, 
        ai_recommendations=ai_recommendations
    )
    
    return AIAnalysisResponse(
        report_id=report_id,
        ai_analysis=ai_analysis,
        ai_recommendations=ai_recommendations,
        confidence_score=0.85,
        processing_time=2.5
    )


@router.put("/{report_id}/status")
def update_report_status(
    report_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新报告状态"""
    # 检查报告是否存在
    existing_report = report_crud.get_report(db, report_id=report_id)
    if not existing_report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    # 检查权限
    if existing_report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限修改此报告")
    
    updated_report = report_crud.update_report_status(db=db, report_id=report_id, status=status)
    if not updated_report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    return {"message": "报告状态更新成功", "status": status} 