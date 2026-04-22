from fastapi import APIRouter, Depends, HTTPException
from app.database import db_dependency
from sqlalchemy import func, select
from app.models.ropa import RopaRecord
from app.schemas.ropa import RopaCreate, RopaResponse
from app.schemas.users import UserCreate, UserResponse
from pwdlib import PasswordHash
from starlette import status
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter(prefix="/processor")

@router.post("/create", response_model=RopaResponse)
async def create_ropa_record(ropa: RopaCreate, db: db_dependency ,user: UserResponse = Depends(get_current_user)):
    new_record = RopaRecord(
        record_type = "Processor",
        status = "Pending",
        request_type = "สร้างรายการใหม่",
        department=user.department,
        processor_name=ropa.processor_name,
        controller_address=ropa.controller_address,
        # Processor Information
        controller_info = ropa.controller_info,
        recorder_email = user.email,
        recorder_phone = user.phone_number,
        recorder_address = user.address,

        # Activity Details
        activity_name = ropa.activity_name,
        purpose = ropa.purpose,
        collected_personal_data = ropa.collected_personal_data,
        data_subject = ropa.data_subject,
        data_type = ropa.data_type,
        collection_format = ropa.collection_format,

        # Sources and legal basis
        is_direct_from_subject = ropa.is_direct_from_subject,
        indirect_source_detail = ropa.indirect_source_detail,
        legal_basis = ropa.legal_basis,
        minor_under_10 = ropa.minor_under_10,
        minor_10_to_20 = ropa.minor_10_to_20,

        # Data transfer and storage
        cb_is_transferred = ropa.cb_is_transferred,
        cb_is_intra_group = ropa.cb_is_intra_group,
        cb_transfer_method = ropa.cb_transfer_method,
        cb_destination_standard = ropa.cb_destination_standard,

        # Retention Policy
        rp_storage_method = ropa.rp_storage_method,
        rp_retention_period = ropa.rp_retention_period,
        rp_access_rights = ropa.rp_access_rights,
        rp_destruction_method = ropa.rp_destruction_method,
        disclosure_without_consent = ropa.disclosure_without_consent,
        dsar_rejection_record = ropa.dsar_rejection_record,

        # Security Measures
        sec_organizational = ropa.sec_organizational,
        sec_technical = ropa.sec_technical,
        sec_physical = ropa.sec_physical,
        sec_access_control = ropa.sec_access_control,
        sec_user_responsibility = ropa.sec_user_responsibility,
        sec_audit_trail = ropa.sec_audit_trail,

        # Audit Fields and Admin Fields
        created_by = user.username,
        created_at = func.current_timestamp(),
        updated_by = user.username,
        updated_at = func.current_timestamp(),
        approved_by = None,
        rejection_reason = None
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/records")
async def get_all_ropa_records(db: db_dependency):
    result = db.execute(select(RopaRecord).where(RopaRecord.record_type == "Processor"))
    records = result.scalars().all()
    return {"records": records }

@router.get("/records/{record_id}", response_model=RopaResponse)
async def get_ropa_record_by_id(record_id: int, db: db_dependency):
    result = db.execute(select(RopaRecord).where(RopaRecord.id == record_id))
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return record

@router.put("/records/{record_id}", response_model=RopaResponse)
async def update_ropa_record(record_id: int, ropa: RopaCreate, db: db_dependency, user: UserResponse = Depends(get_current_user)):
    result = db.execute(select(RopaRecord).where(RopaRecord.id == record_id))
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    record.status=ropa.status
    record.controller_info = ropa.controller_info
    record.recorder_email = user.email
    record.recorder_phone = user.phone_number
    record.recorder_address = user.address
    record.activity_name = ropa.activity_name
    record.purpose = ropa.purpose
    record.collected_personal_data = ropa.collected_personal_data
    record.data_subject = ropa.data_subject
    record.data_type = ropa.data_type
    record.collection_format = ropa.collection_format
    record.is_direct_from_subject = ropa.is_direct_from_subject
    record.indirect_source_detail = ropa.indirect_source_detail
    record.legal_basis = ropa.legal_basis
    record.minor_under_10 = ropa.minor_under_10
    record.minor_10_to_20 = ropa.minor_10_to_20
    record.cb_is_transferred = ropa.cb_is_transferred
    record.cb_is_intra_group = ropa.cb_is_intra_group
    record.cb_transfer_method = ropa.cb_transfer_method
    record.cb_destination_standard = ropa.cb_destination_standard
    record.rp_storage_method = ropa.rp_storage_method
    record.rp_retention_period = ropa.rp_retention_period
    record.rp_access_rights = ropa.rp_access_rights
    record.rp_destruction_method = ropa.rp_destruction_method
    record.disclosure_without_consent = ropa.disclosure_without_consent
    record.dsar_rejection_record = ropa.dsar_rejection_record
    record.sec_organizational = ropa.sec_organizational
    record.sec_technical = ropa.sec_technical
    record.sec_physical = ropa.sec_physical
    record.sec_access_control = ropa.sec_access_control
    record.sec_user_responsibility = ropa.sec_user_responsibility
    record.sec_audit_trail = ropa.sec_audit_trail
    record.updated_by = user.username
    record.updated_at = func.current_timestamp()
    record.approved_by = None
    record.rejection_reason = None


    db.commit()
    db.refresh(record)
    return record

@router.delete("/records/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ropa_record(record_id: int, db: db_dependency):
    result = db.execute(select(RopaRecord).where(RopaRecord.id == record_id))
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    db.delete(record)
    db.commit()