from fastapi import APIRouter, Depends, HTTPException
from app.database import db_dependency
from sqlalchemy import func, select
from app.models.ropa import RopaRecord
from app.schemas.ropa import RopaCreate, RopaResponse
from app.schemas.users import UserCreate, UserResponse
from pwdlib import PasswordHash
from starlette import status
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter(prefix="/controller")

@router.post("/create", response_model=RopaResponse)
async def create_ropa_record(ropa: RopaCreate, db: db_dependency ,user: UserResponse = Depends(get_current_user)):
    new_record = RopaRecord(
        record_type="Controller",
        status="Pending",
        request_type="สร้างรายการใหม่",
        department=user.department,

        # Controller Information
        controller_info=ropa.controller_info,
        recorder_email=user.email,
        recorder_phone=user.phone_number,
        recorder_address=user.address,

        # Activity Details
        activity_name=ropa.activity_name,
        purpose=ropa.purpose,
        collected_personal_data=ropa.collected_personal_data,
        data_subject=ropa.data_subject,
        data_type=ropa.data_type,
        collection_format=ropa.collection_format,

        # Sources and legal basis
        is_direct_from_subject=ropa.is_direct_from_subject,
        indirect_source_detail=ropa.indirect_source_detail,
        legal_basis=ropa.legal_basis,
        minor_under_10=ropa.minor_under_10,
        minor_10_to_20=ropa.minor_10_to_20,

        # Data transfer and storage
        cb_is_transferred=ropa.cb_is_transferred,
        cb_is_intra_group=ropa.cb_is_intra_group,
        cb_transfer_method=ropa.cb_transfer_method,
        cb_destination_standard=ropa.cb_destination_standard,

        # Retention Policy
        rp_storage_method=ropa.rp_storage_method,
        rp_retention_period=ropa.rp_retention_period,
        rp_access_rights=ropa.rp_access_rights,
        rp_destruction_method=ropa.rp_destruction_method,
        disclosure_without_consent=ropa.disclosure_without_consent,
        dsar_rejection_record=ropa.dsar_rejection_record,

        # Security Measures
        sec_organizational=ropa.sec_organizational,
        sec_technical=ropa.sec_technical,
        sec_physical=ropa.sec_physical,
        sec_access_control=ropa.sec_access_control,
        sec_user_responsibility=ropa.sec_user_responsibility,
        sec_audit_trail=ropa.sec_audit_trail,

        # Audit Logs & Admin Fields
        created_by=user.username,
        created_at=func.now(),
        updated_by=user.username,
        updated_at=func.now(),
        approved_by=None,
        rejection_reason=None
    )
    db.add(new_record) #add to database
    db.commit()
    db.refresh(new_record) #refresh to get the new record from database after commit
    return new_record

@router.post("/mock_create", response_model=RopaResponse)
async def mock_create_ropa_record(ropa: RopaCreate, db: db_dependency):
    new_record = RopaRecord(
        record_type="Controller",
        status="Pending",

        # Controller Information
        controller_info=ropa.controller_info,
        controller_name="John Doe",
        email="johndoe@example.com",
        phone="+1234567890",
        controller_address="123 Main St, City, State 12345",
        
        # Activity Details
        activity_name=ropa.activity_name,
        purpose=ropa.purpose,
        collected_personal_data=ropa.collected_personal_data,
        data_subject=ropa.data_subject,
        data_type=ropa.data_type,
        collection_format=ropa.collection_format,

        # Sources and legal basis
        is_direct_from_subject=ropa.is_direct_from_subject,
        indirect_source_detail=ropa.indirect_source_detail,
        legal_basis=ropa.legal_basis,
        minor_under_10=ropa.minor_under_10,
        minor_10_to_20=ropa.minor_10_to_20,

        # Data transfer and storage
        cb_is_transferred=ropa.cb_is_transferred,
        cb_is_intra_group=ropa.cb_is_intra_group,
        cb_transfer_method=ropa.cb_transfer_method,
        cb_destination_standard=ropa.cb_destination_standard,

        # Retention Policy
        rp_storage_method=ropa.rp_storage_method,
        rp_retention_period=ropa.rp_retention_period,
        rp_access_rights=ropa.rp_access_rights,
        rp_destruction_method=ropa.rp_destruction_method,
        disclosure_without_consent=ropa.disclosure_without_consent,
        dsar_rejection_record=ropa.dsar_rejection_record,

        # Security Measures
        sec_organizational=ropa.sec_organizational,
        sec_technical=ropa.sec_technical,
        sec_physical=ropa.sec_physical,
        sec_access_control=ropa.sec_access_control,
        sec_user_responsibility=ropa.sec_user_responsibility,
        sec_audit_trail=ropa.sec_audit_trail,

        # Audit Logs & Admin Fields
        created_by="John Doe",
        created_at=func.now(),
        updated_by="John Doe",
        updated_at=func.now(),
        approved_by=None,
        rejection_reason=None
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/records")
async def get_all_ropa_records(db: db_dependency):
    result = db.execute(select(RopaRecord).where(RopaRecord.record_type=="Controller"))
    records = result.scalars().all()
    return {"records": records}

@router.get("/records/{record_id}", response_model=RopaResponse)
async def get_ropa_record_by_id(record_id: int, db: db_dependency):
    result = db.execute(select(RopaRecord).where(RopaRecord.id == record_id))
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return record

@router.put("/records/{record_id}", response_model=RopaResponse)
async def update_ropa_record(record_id: int, ropa_update: RopaCreate, db: db_dependency):
    result = db.execute(select(RopaRecord).where(RopaRecord.id == record_id))
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    
    # Update fields
    record.department=ropa_update.department,
    record.status = ropa_update.status
    record.processor_name = ropa_update.processor_name
    record.controller_info = ropa_update.controller_info
    record.activity_name = ropa_update.activity_name
    record.purpose = ropa_update.purpose
    record.collected_personal_data = ropa_update.collected_personal_data
    record.data_subject = ropa_update.data_subject
    record.data_type = ropa_update.data_type
    record.collection_format = ropa_update.collection_format
    record.is_direct_from_subject = ropa_update.is_direct_from_subject
    record.indirect_source_detail = ropa_update.indirect_source_detail
    record.legal_basis = ropa_update.legal_basis
    record.minor_under_10 = ropa_update.minor_under_10
    record.minor_10_to_20 = ropa_update.minor_10_to_20
    record.cb_is_transferred = ropa_update.cb_is_transferred
    record.cb_is_intra_group = ropa_update.cb_is_intra_group
    record.cb_transfer_method = ropa_update.cb_transfer_method
    record.cb_destination_standard = ropa_update.cb_destination_standard
    record.rp_storage_method = ropa_update.rp_storage_method
    record.rp_retention_period = ropa_update.rp_retention_period
    record.rp_access_rights = ropa_update.rp_access_rights
    record.rp_destruction_method = ropa_update.rp_destruction_method
    record.disclosure_without_consent = ropa_update.disclosure_without_consent
    record.dsar_rejection_record = ropa_update.dsar_rejection_record
    record.sec_organizational = ropa_update.sec_organizational
    record.sec_technical = ropa_update.sec_technical
    record.sec_physical = ropa_update.sec_physical
    record.sec_access_control = ropa_update.sec_access_control
    record.sec_user_responsibility = ropa_update.sec_user_responsibility
    record.sec_audit_trail = ropa_update.sec_audit_trail

    db.commit()
    db.refresh(record)
    return record

@router.delete("/records/{record_id}")
async def delete_ropa_record(record_id: int, db: db_dependency):
    result = db.execute(select(RopaRecord).where(RopaRecord.id == record_id))
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    db.delete(record)
    db.commit()
    return {"detail": f"Record ID:{record_id} deleted successfully"}

