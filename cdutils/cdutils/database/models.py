from typing import Optional

from sqlalchemy import CHAR, CheckConstraint, Column, DateTime, Double, Index, Integer, PrimaryKeyConstraint, Table, Text, VARCHAR, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime
import decimal

class Base(DeclarativeBase):
    pass


t_acctavailamthist = Table(
    'acctavailamthist', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False),
    Column('subacctnbr', NUMBER(22, 0, False), nullable=False),
    Column('effdate', DateTime, nullable=False),
    Column('availincrcd', VARCHAR(4), nullable=False),
    Column('availdate', DateTime, nullable=False),
    Column('availamt', NUMBER(22, 3, True), nullable=False),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE ')),
    schema='COCCDM'
)


class Acctdrawacct(Base):
    __tablename__ = 'acctdrawacct'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'drawacctnbr', name='pk_acctdrawacct'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Account Number is the system assigned primary key that uniquely identifies each account.')
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, comment='The Effective Date is the date the draw becomes active.')
    drawacctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Draw Account Number is the account number for the draw.')
    drawseq: Mapped[float] = mapped_column(NUMBER(22, 0, False), comment='The Draw Sequence is the order by which the account is used for the draw.')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM  USE  ONLY')
    inactivedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The Inactive Date is the date that the draw becomes inactive.')
    mindrawamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True), comment='Sets the minimum amount allowable for a draw (overdraft protection). Overdrafts below this amount will not trigger draws.')
    drawbalgoalamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True), comment='Sets the balance amount that the draw will try to meet or exceed. This is the amount in the drawing, or protected account.')
    drawincramt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True), comment='Sets amount of overdraft protection draws. Withdrawals or advances for overdraft protection will be a multiple of this amount.')


class Acctmemobaltyp(Base):
    __tablename__ = 'acctmemobaltyp'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'memobaltypcd', name='pk_acctmemobaltyp'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    memobaltypcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    balamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))


class Acctpropins(Base):
    __tablename__ = 'acctpropins'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'propnbr', 'intrpolicynbr', name='pk_acctpropins'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    propnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    intrpolicynbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    escrowyn: Mapped[str] = mapped_column(CHAR(1))
    lenderfundedyn: Mapped[str] = mapped_column(CHAR(1))
    effdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    inactivedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class Accttitle(Base):
    __tablename__ = 'accttitle'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'accttitlelinenbr', name='pk_accttitle'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    accttitlelinenbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    accttitlelinetext: Mapped[Optional[str]] = mapped_column(VARCHAR(40))


class Acctuserfield(Base):
    __tablename__ = 'acctuserfield'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'userfieldcd', name='pk_acctuserfield'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    userfieldcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    value: Mapped[Optional[str]] = mapped_column(VARCHAR(254))


class Acctwrn(Base):
    __tablename__ = 'acctwrn'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'effdate', 'wrnflagcd', name='pk_acctwrn'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    wrnflagcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    notenbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    inactivedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class Achwhitelist(Base):
    __tablename__ = 'achwhitelist'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'whitelistnbr', name='pk_achwhitelist'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='Account Number')
    whitelistnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='Index for WhiteList within the Account')
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('sysdate '), comment='Effective date')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('sysdate '), comment='System Generated Date')
    sourceid: Mapped[Optional[str]] = mapped_column(VARCHAR(20), comment='Source ID')
    sourcename: Mapped[Optional[str]] = mapped_column(VARCHAR(40), comment='Source Name')
    achseccd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='SEC ')
    minamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True), comment='Minimum amount ')
    maxamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True), comment='Maximum amount')
    inactivedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='Inactive date')
    reasoncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Reason Code')
    contact: Mapped[Optional[str]] = mapped_column(VARCHAR(2000), comment='Contact Information')


t_addruse = Table(
    'addruse', Base.metadata,
    Column('addrusecd', VARCHAR(4), nullable=False),
    Column('addrusedesc', VARCHAR(30), nullable=False),
    Column('datelastmaint', DateTime, nullable=False),
    Column('electronicyn', CHAR(1), nullable=False),
    Column('desctokennbr', NUMBER(22, 0, False)),
    Column('descnamespacecd', VARCHAR(4)),
    schema='COCCDM'
)


class Agreepersaccesstypacct(Base):
    __tablename__ = 'agreepersaccesstypacct'
    __table_args__ = (
        PrimaryKeyConstraint('agreenbr', 'persnbr', 'accesstypcd', 'acctnbr', name='pk_agreepersacctaccesstyp'),
        {'schema': 'COCCDM'}
    )

    agreenbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    persnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    accesstypcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    allowedyn: Mapped[Optional[str]] = mapped_column(CHAR(1))


t_au_actiontaken = Table(
    'au_actiontaken', Base.metadata,
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('actiontaken', VARCHAR(256)),
    schema='COCCDM'
)


t_au_commontable = Table(
    'au_commontable', Base.metadata,
    Column('auditid', NUMBER(19, 0, False), nullable=False),
    Column('commonid', VARCHAR(40)),
    Column('logdate', DateTime),
    Column('userid', VARCHAR(256)),
    Column('hostname', VARCHAR(256)),
    Column('ipaddress', VARCHAR(256)),
    Column('url', VARCHAR(256)),
    Column('urlreferer', VARCHAR(256)),
    Column('browser', VARCHAR(256)),
    Column('useragent', NUMBER(10, 0, False), nullable=False),
    Column('usersessionid', VARCHAR(256)),
    Column('actiontaken', NUMBER(10, 0, False)),
    Column('result', VARCHAR(5)),
    Column('message', VARCHAR(256)),
    Column('logdateudt', DateTime),
    Column('details', VARCHAR(2048)),
    Column('credentials', VARCHAR(100)),
    Column('dataspace', VARCHAR(10)),
    schema='COCCDM'
)


t_au_commontable_temp = Table(
    'au_commontable_temp', Base.metadata,
    Column('auditid', NUMBER(19, 0, False), nullable=False),
    Column('commonid', VARCHAR(40)),
    Column('logdate', DateTime),
    Column('userid', VARCHAR(256)),
    Column('hostname', VARCHAR(256)),
    Column('ipaddress', VARCHAR(256)),
    Column('url', VARCHAR(256)),
    Column('urlreferer', VARCHAR(256)),
    Column('browser', VARCHAR(256)),
    Column('useragent', NUMBER(10, 0, False), nullable=False),
    Column('usersessionid', VARCHAR(256)),
    Column('actiontaken', NUMBER(10, 0, False)),
    Column('result', VARCHAR(5)),
    Column('message', VARCHAR(256)),
    Column('logdateudt', DateTime),
    Column('details', VARCHAR(2048)),
    Column('credentials', VARCHAR(100)),
    Column('dataspace', VARCHAR(10)),
    schema='COCCDM'
)


t_au_commontable_view = Table(
    'au_commontable_view', Base.metadata,
    Column('auditid', NUMBER(19, 0, False), nullable=False),
    Column('commonid', VARCHAR(40)),
    Column('logdate', DateTime),
    Column('dataspace', VARCHAR(10)),
    Column('actiontaken', VARCHAR(256)),
    Column('hostname', VARCHAR(256)),
    Column('ipaddress', VARCHAR(256)),
    Column('url', VARCHAR(256)),
    Column('urlreferer', VARCHAR(256)),
    Column('browser', VARCHAR(256)),
    Column('useragent', NUMBER(10, 0, False), nullable=False),
    Column('usersessionid', VARCHAR(256)),
    Column('result', VARCHAR(5)),
    Column('message', VARCHAR(256)),
    Column('logdateudt', DateTime),
    Column('details', VARCHAR(2048)),
    Column('credentials', VARCHAR(100)),
    Column('userid', VARCHAR(256)),
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('value', VARCHAR(1000)),
    Column('deviceid', VARCHAR(80)),
    Column('ismobiledevice', VARCHAR(5)),
    Column('platform', VARCHAR(40)),
    Column('platformversion', VARCHAR(40)),
    Column('browserversion', VARCHAR(40)),
    schema='COCCDM'
)


t_au_commontable_view_temp = Table(
    'au_commontable_view_temp', Base.metadata,
    Column('auditid', NUMBER(19, 0, False), nullable=False),
    Column('commonid', VARCHAR(40)),
    Column('logdate', DateTime),
    Column('dataspace', VARCHAR(10)),
    Column('actiontaken', VARCHAR(256)),
    Column('hostname', VARCHAR(256)),
    Column('ipaddress', VARCHAR(256)),
    Column('url', VARCHAR(256)),
    Column('urlreferer', VARCHAR(256)),
    Column('browser', VARCHAR(256)),
    Column('useragent', NUMBER(10, 0, False), nullable=False),
    Column('usersessionid', VARCHAR(256)),
    Column('result', VARCHAR(5)),
    Column('message', VARCHAR(256)),
    Column('logdateudt', DateTime),
    Column('details', VARCHAR(2048)),
    Column('credentials', VARCHAR(100)),
    Column('userid', VARCHAR(256)),
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('value', VARCHAR(1000)),
    Column('deviceid', VARCHAR(80)),
    Column('ismobiledevice', VARCHAR(5)),
    Column('platform', VARCHAR(40)),
    Column('platformversion', VARCHAR(40)),
    Column('browserversion', VARCHAR(40)),
    schema='COCCDM'
)


t_au_ftsologs = Table(
    'au_ftsologs', Base.metadata,
    Column('auditid', NUMBER(19, 0, False), nullable=False),
    Column('score', NUMBER(10, 0, False)),
    Column('tries', NUMBER(10, 0, False)),
    Column('failedreason', VARCHAR(256)),
    Column('field', VARCHAR(256)),
    Column('accountid', VARCHAR(100)),
    Column('firstname', VARCHAR(256)),
    Column('lastname', VARCHAR(256)),
    schema='COCCDM'
)


t_au_hb_checkview = Table(
    'au_hb_checkview', Base.metadata,
    Column('auditid', NUMBER(19, 0, False), nullable=False),
    Column('checkviewid', VARCHAR(40)),
    Column('accountid', VARCHAR(256)),
    Column('accounttype', VARCHAR(256)),
    Column('amount', NUMBER(17, 4, True)),
    Column('checknum', VARCHAR(256)),
    Column('tracenum', VARCHAR(256)),
    Column('postdate', DateTime),
    Column('effectivedate', DateTime),
    Column('checksideview', VARCHAR(256)),
    Column('accountnumber', VARCHAR(50)),
    schema='COCCDM'
)


t_au_sms_log = Table(
    'au_sms_log', Base.metadata,
    Column('auditid', NUMBER(19, 0, False), nullable=False),
    Column('phonenumber', VARCHAR(24)),
    Column('smscommand', VARCHAR(20)),
    schema='COCCDM'
)


t_au_stoppaymentlogs = Table(
    'au_stoppaymentlogs', Base.metadata,
    Column('auditid', NUMBER(19, 0, False), nullable=False),
    Column('accountid', VARCHAR(64)),
    Column('description', VARCHAR(100)),
    Column('amount', NUMBER(18, 2, True), nullable=False),
    Column('startcheck', NUMBER(10, 0, False), nullable=False),
    Column('endcheck', NUMBER(10, 0, False), nullable=False),
    Column('accountnumber', VARCHAR(50)),
    Column('payee', VARCHAR(256)),
    Column('reason', VARCHAR(256)),
    schema='COCCDM'
)


t_au_useragent = Table(
    'au_useragent', Base.metadata,
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('value', VARCHAR(900)),
    Column('deviceid', VARCHAR(80)),
    Column('ismobiledevice', VARCHAR(5)),
    Column('platform', VARCHAR(40)),
    Column('platformversion', VARCHAR(40)),
    Column('browser', VARCHAR(40)),
    Column('browserversion', VARCHAR(40)),
    Column('source', VARCHAR(14)),
    Column('devicetype', VARCHAR(14)),
    schema='COCCDM'
)


t_au_userprofilechange = Table(
    'au_userprofilechange', Base.metadata,
    Column('auditid', NUMBER(19, 0, False), nullable=False),
    Column('fieldname', VARCHAR(100)),
    Column('oldvalue', VARCHAR(100)),
    Column('newvalue', VARCHAR(100)),
    Column('explanation', VARCHAR(256)),
    schema='COCCDM'
)


t_au_xfr_account = Table(
    'au_xfr_account', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('type', VARCHAR(20)),
    schema='COCCDM'
)


t_au_xfr_achaccount = Table(
    'au_xfr_achaccount', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('userid', VARCHAR(32)),
    Column('institutionname', VARCHAR(36)),
    Column('routingnumber', VARCHAR(9)),
    Column('accountnumber', VARCHAR(17)),
    Column('accounttype', VARCHAR(20)),
    schema='COCCDM'
)


t_au_xfr_achtransfer = Table(
    'au_xfr_achtransfer', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('individualname', VARCHAR(22)),
    Column('riskscore', NUMBER(10, 0, False), nullable=False),
    Column('institutionuserid', VARCHAR(32)),
    Column('externalinstitutionname', VARCHAR(36)),
    Column('externalroutingnumber', VARCHAR(9)),
    Column('externalachaccountnumber', VARCHAR(24)),
    Column('externalachaccounttype', VARCHAR(20)),
    Column('internalaccountnumber', VARCHAR(40)),
    Column('internalachaccountnumber', VARCHAR(24)),
    Column('internalachaccounttype', VARCHAR(20)),
    Column('recurring', VARCHAR(5)),
    schema='COCCDM'
)


t_au_xfr_entchangesetproperty_v = Table(
    'au_xfr_entchangesetproperty_v', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('entitychangesetid', NUMBER(19, 0, False), nullable=False),
    Column('childentitytypename', VARCHAR(50)),
    Column('childentityid', NUMBER(19, 0, False)),
    Column('entitypropertyname', VARCHAR(50)),
    Column('oldvalue', Text),
    Column('newvalue', Text),
    schema='COCCDM'
)


t_au_xfr_entitychangeset = Table(
    'au_xfr_entitychangeset', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('auditid', NUMBER(19, 0, False), nullable=False),
    Column('entitytypeid', NUMBER(5, 0, False), nullable=False),
    Column('entitydataspace', VARCHAR(10)),
    Column('entityid', NUMBER(19, 0, False), nullable=False),
    schema='COCCDM'
)


t_au_xfr_entitychangeset_view = Table(
    'au_xfr_entitychangeset_view', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('entitytypename', VARCHAR(50)),
    Column('entitydataspace', VARCHAR(10)),
    Column('entityid', NUMBER(19, 0, False), nullable=False),
    Column('auditid', NUMBER(19, 0, False), nullable=False),
    schema='COCCDM'
)


t_au_xfr_entitychangesetproperty = Table(
    'au_xfr_entitychangesetproperty', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('entitychangesetid', NUMBER(19, 0, False), nullable=False),
    Column('childentitytypeid', NUMBER(5, 0, False)),
    Column('childentityid', NUMBER(19, 0, False)),
    Column('entitypropertyid', NUMBER(5, 0, False), nullable=False),
    Column('oldvalue', Text),
    Column('newvalue', Text),
    schema='COCCDM'
)


t_au_xfr_entityproperty = Table(
    'au_xfr_entityproperty', Base.metadata,
    Column('id', NUMBER(5, 0, False), nullable=False),
    Column('name', VARCHAR(50)),
    schema='COCCDM'
)


t_au_xfr_entitytype = Table(
    'au_xfr_entitytype', Base.metadata,
    Column('id', NUMBER(5, 0, False), nullable=False),
    Column('name', VARCHAR(50)),
    schema='COCCDM'
)


t_au_xfr_hostaccount = Table(
    'au_xfr_hostaccount', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('hostaccountid', VARCHAR(64)),
    Column('achaccountnumber', VARCHAR(24)),
    Column('achaccounttype', VARCHAR(20)),
    Column('regdlimited', VARCHAR(5)),
    Column('accountnumber', VARCHAR(40)),
    schema='COCCDM'
)


t_au_xfr_hosttransfertxn = Table(
    'au_xfr_hosttransfertxn', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('hosttransactionid', VARCHAR(20)),
    Column('executiondatetimeutc', DateTime, nullable=False),
    Column('succeeded', VARCHAR(5)),
    Column('failurereason', VARCHAR(1000)),
    schema='COCCDM'
)


t_au_xfr_hosttransfertxn_temp = Table(
    'au_xfr_hosttransfertxn_temp', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('hosttransactionid', VARCHAR(20)),
    Column('executiondatetimeutc', DateTime, nullable=False),
    Column('succeeded', VARCHAR(5)),
    Column('failurereason', VARCHAR(1000)),
    schema='COCCDM'
)


t_au_xfr_hosttransfertxn_v = Table(
    'au_xfr_hosttransfertxn_v', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('scheduledtransferid', NUMBER(19, 0, False)),
    Column('hosttransfertransactionid', NUMBER(19, 0, False), nullable=False),
    Column('hosttransactionid', VARCHAR(20)),
    Column('sourcehostaccountid', VARCHAR(50)),
    Column('sourcehostaccountnumber', VARCHAR(40)),
    Column('destinationhostaccountid', VARCHAR(50)),
    Column('destinationhostaccountnumber', VARCHAR(40)),
    Column('amount', NUMBER(19, 4, True), nullable=False),
    Column('succeeded', VARCHAR(5)),
    schema='COCCDM'
)


t_au_xfr_schedhosttransfer_v = Table(
    'au_xfr_schedhosttransfer_v', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('scheduledtransferid', NUMBER(19, 0, False), nullable=False),
    Column('sourcehostaccountid', VARCHAR(50)),
    Column('sourcehostaccountnumber', VARCHAR(40)),
    Column('destinationhostaccountid', VARCHAR(50)),
    Column('destinationhostaccountnumber', VARCHAR(40)),
    schema='COCCDM'
)


t_au_xfr_scheduledtransfer = Table(
    'au_xfr_scheduledtransfer', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('type', VARCHAR(20)),
    Column('userid', VARCHAR(32)),
    Column('sourceaccountid', NUMBER(19, 0, False), nullable=False),
    Column('destinationaccountid', NUMBER(19, 0, False), nullable=False),
    Column('creationdatetime', DateTime, nullable=False),
    Column('creationdatetimeutc', DateTime, nullable=False),
    schema='COCCDM'
)


t_au_xfr_transaction = Table(
    'au_xfr_transaction', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('type', VARCHAR(20)),
    Column('parenttransferid', NUMBER(19, 0, False), nullable=False),
    schema='COCCDM'
)


t_au_xfr_transfer = Table(
    'au_xfr_transfer', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('type', VARCHAR(20)),
    Column('userid', VARCHAR(32)),
    Column('sourceaccountid', NUMBER(19, 0, False)),
    Column('destinationaccountid', NUMBER(19, 0, False)),
    Column('paymenttype', VARCHAR(20)),
    Column('amount', NUMBER(19, 4, True), nullable=False),
    Column('description', VARCHAR(120)),
    Column('sendsuccessnotification', VARCHAR(5)),
    Column('scheduledtransferid', NUMBER(19, 0, False)),
    Column('rundatetime', DateTime, nullable=False),
    Column('rundatetimeutc', DateTime, nullable=False),
    Column('submittedbyuserid', VARCHAR(32)),
    Column('contributionyear', VARCHAR(20)),
    schema='COCCDM'
)


t_au_xfr_transfer_temp = Table(
    'au_xfr_transfer_temp', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('type', VARCHAR(20)),
    Column('userid', VARCHAR(32)),
    Column('sourceaccountid', NUMBER(19, 0, False)),
    Column('destinationaccountid', NUMBER(19, 0, False)),
    Column('paymenttype', VARCHAR(20)),
    Column('amount', NUMBER(19, 4, True), nullable=False),
    Column('description', VARCHAR(120)),
    Column('sendsuccessnotification', VARCHAR(5)),
    Column('scheduledtransferid', NUMBER(19, 0, False)),
    Column('rundatetime', DateTime, nullable=False),
    Column('rundatetimeutc', DateTime, nullable=False),
    Column('submittedbyuserid', VARCHAR(32)),
    Column('contributionyear', VARCHAR(20)),
    schema='COCCDM'
)


t_au_xfr_unlinkedaccount = Table(
    'au_xfr_unlinkedaccount', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('userid', VARCHAR(32)),
    Column('hostaccountid', VARCHAR(64)),
    Column('achaccountnumber', VARCHAR(24)),
    Column('achaccounttype', VARCHAR(20)),
    Column('regdlimited', VARCHAR(5)),
    Column('accountnumber', VARCHAR(40)),
    schema='COCCDM'
)


t_availincr = Table(
    'availincr', Base.metadata,
    Column('availincrcd', VARCHAR(4), nullable=False),
    Column('availincrdesc', VARCHAR(30), nullable=False),
    Column('availamt', NUMBER(15, 2, True)),
    Column('availdurcd', VARCHAR(4)),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE ')),
    schema='COCCDM'
)


t_bank_achbatch = Table(
    'bank_achbatch', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('refnum', NUMBER(19, 0, False), nullable=False),
    Column('batchtemplateid', NUMBER(19, 0, False), nullable=False),
    Column('batchname', VARCHAR(40)),
    Column('companyid', NUMBER(19, 0, False), nullable=False),
    Column('companyname', VARCHAR(16)),
    Column('companyidentifier', VARCHAR(20)),
    Column('transactiontype', NUMBER(10, 0, False), nullable=False),
    Column('companydiscretionarydata', VARCHAR(20)),
    Column('companyentrydescription', VARCHAR(40)),
    Column('offsetaccountid', VARCHAR(64)),
    Column('offsetaccountnumber', VARCHAR(40)),
    Column('offsetaccountnickname', VARCHAR(40)),
    Column('isprenote', VARCHAR(5)),
    Column('effectivedate', DateTime, nullable=False),
    Column('status', NUMBER(10, 0, False), nullable=False),
    Column('masteruserid', VARCHAR(10)),
    Column('dataspace', VARCHAR(10)),
    Column('businessname', VARCHAR(256)),
    Column('initiatoruserid', VARCHAR(10)),
    Column('initiateddate', DateTime),
    Column('firstapproveruserid', VARCHAR(10)),
    Column('firstapproveddate', DateTime),
    Column('rejecteruserid', VARCHAR(10)),
    Column('rejecteddate', DateTime),
    Column('cancelleruserid', VARCHAR(10)),
    Column('cancelleddate', DateTime),
    Column('achbatchfileid', VARCHAR(10)),
    Column('recorddeleted', VARCHAR(5)),
    Column('insertenterprisedate', DateTime, nullable=False),
    Column('updateenterprisedate', DateTime, nullable=False),
    Column('secondapproveruserid', VARCHAR(10)),
    Column('secondapproveddate', DateTime),
    Column('approvalsrequired', NUMBER(3, 0, False)),
    Column('issameday', VARCHAR(5)),
    Column('scheduleinfo', NUMBER(5, 0, False)),
    Column('updatecomment', Text),
    Column('achaccountnumber', VARCHAR(40)),
    Column('achtransactioncode', VARCHAR(10)),
    Column('prefundingstatus', NUMBER(5, 0, False)),
    Column('holdid', VARCHAR(50)),
    Column('isrestricted', VARCHAR(5)),
    Column('offsetindividually', VARCHAR(5)),
    Column('alternateoffsetaccountnumber', VARCHAR(24)),
    Column('alternateoffsetaccounttype', NUMBER(3, 0, False)),
    Column('sweeptransactionid', VARCHAR(30)),
    Column('useparticipantdistributions', VARCHAR(5)),
    Column('sweepreversaltransactionid', VARCHAR(30)),
    schema='COCCDM'
)


t_bank_achbatchtemplate = Table(
    'bank_achbatchtemplate', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('batchname', VARCHAR(40)),
    Column('companyid', NUMBER(19, 0, False), nullable=False),
    Column('transactiontype', NUMBER(10, 0, False), nullable=False),
    Column('companydiscretionarydata', VARCHAR(20)),
    Column('companyentrydescription', VARCHAR(10)),
    Column('offsetaccountid', VARCHAR(64)),
    Column('effectivedate', DateTime),
    Column('masteruserid', VARCHAR(50)),
    Column('recorddeleted', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('updatedateutc', DateTime, nullable=False),
    Column('isrestricted', VARCHAR(5)),
    Column('offsetindividually', VARCHAR(5)),
    Column('useparticipantdistributions', VARCHAR(5)),
    schema='COCCDM'
)


t_bank_achcompany = Table(
    'bank_achcompany', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('identifiertype', NUMBER(5, 0, False)),
    Column('identifier', VARCHAR(20)),
    Column('companyname', VARCHAR(16)),
    Column('description', VARCHAR(80)),
    Column('masteruserid', VARCHAR(50)),
    Column('recorddeleted', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('updatedateutc', DateTime, nullable=False),
    schema='COCCDM'
)


t_bank_achentry = Table(
    'bank_achentry', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('batchid', NUMBER(19, 0, False), nullable=False),
    Column('entrytemplateid', NUMBER(19, 0, False), nullable=False),
    Column('participantid', NUMBER(19, 0, False)),
    Column('amount', NUMBER(18, 2, True), nullable=False),
    Column('paymenttype', NUMBER(10, 0, False), nullable=False),
    Column('participantname', VARCHAR(22)),
    Column('nickname', VARCHAR(40)),
    Column('uniqueidentifier', VARCHAR(15)),
    Column('accountnumber', VARCHAR(24)),
    Column('routingnumber', VARCHAR(9)),
    Column('accounttype', NUMBER(10, 0, False), nullable=False),
    Column('discretionarydata', VARCHAR(2)),
    Column('category', VARCHAR(40)),
    Column('masteruserid', VARCHAR(50)),
    Column('recorddeleted', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('updatedateutc', DateTime, nullable=False),
    Column('memo', Text),
    Column('ischildsupportparticipant', VARCHAR(5)),
    Column('childsupportcaseidentifier', VARCHAR(10)),
    Column('childsupportssn', VARCHAR(9)),
    Column('childsupportemploymentstatus', NUMBER(3, 0, False)),
    Column('childsupportmedicalinsstat', NUMBER(3, 0, False)),
    Column('childsupportfipscode', VARCHAR(5)),
    Column('notifyparticipant', VARCHAR(5)),
    schema='COCCDM'
)


t_bank_achentrytemplate = Table(
    'bank_achentrytemplate', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('batchtemplateid', NUMBER(19, 0, False), nullable=False),
    Column('participantid', NUMBER(19, 0, False)),
    Column('amount', NUMBER(18, 2, True)),
    Column('uniqueidentifier', VARCHAR(15)),
    Column('paymenttype', NUMBER(10, 0, False), nullable=False),
    Column('hold', VARCHAR(5)),
    Column('prenote', VARCHAR(5)),
    Column('prenotedate', DateTime),
    Column('prenotebatchid', NUMBER(19, 0, False)),
    Column('recorddeleted', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('updatedateutc', DateTime, nullable=False),
    Column('memo', Text),
    Column('notifyparticipant', VARCHAR(5)),
    schema='COCCDM'
)


t_bank_achparticipant = Table(
    'bank_achparticipant', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('name', VARCHAR(22)),
    Column('nickname', VARCHAR(40)),
    Column('institutionname', VARCHAR(36)),
    Column('uniqueidentifier', VARCHAR(15)),
    Column('accountnumber', VARCHAR(24)),
    Column('routingnumber', VARCHAR(9)),
    Column('accounttype', NUMBER(10, 0, False), nullable=False),
    Column('status', NUMBER(10, 0, False), nullable=False),
    Column('category', VARCHAR(40)),
    Column('memo', VARCHAR(80)),
    Column('discretionarydata', VARCHAR(2)),
    Column('masteruserid', VARCHAR(50)),
    Column('recorddeleted', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('updatedateutc', DateTime, nullable=False),
    Column('ischildsupportparticipant', VARCHAR(5)),
    Column('childsupportcaseidentifier', VARCHAR(10)),
    Column('childsupportssn', VARCHAR(9)),
    Column('childsupportemploymentstatus', NUMBER(3, 0, False)),
    Column('childsupportmedicalinsstat', NUMBER(3, 0, False)),
    Column('childsupportfipscode', VARCHAR(5)),
    Column('emailaddress', VARCHAR(256)),
    Column('notifyparticipantbydefault', VARCHAR(5)),
    schema='COCCDM'
)


t_bank_business = Table(
    'bank_business', Base.metadata,
    Column('masteruserid', NUMBER(19, 0, False), nullable=False),
    Column('businessuserid', NUMBER(19, 0, False), nullable=False),
    schema='COCCDM'
)


t_bank_user = Table(
    'bank_user', Base.metadata,
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('institutionid', NUMBER(19, 0, False), nullable=False),
    Column('institutionuserid', VARCHAR(32)),
    Column('recorddeleted', VARCHAR(5)),
    Column('refreshdateutc', DateTime),
    Column('lockacquireddateutc', DateTime),
    Column('lasthostrefreshstartdttm', DateTime),
    schema='COCCDM'
)


t_bank_userrelationship = Table(
    'bank_userrelationship', Base.metadata,
    Column('masteruserid', NUMBER(19, 0, False), nullable=False),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    schema='COCCDM'
)


t_bank_v_achbatch = Table(
    'bank_v_achbatch', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('refnum', NUMBER(19, 0, False), nullable=False),
    Column('batchtemplateid', NUMBER(19, 0, False), nullable=False),
    Column('batchname', VARCHAR(40)),
    Column('companyid', NUMBER(19, 0, False), nullable=False),
    Column('companyname', VARCHAR(16)),
    Column('companyidentifier', VARCHAR(20)),
    Column('transactiontype', NUMBER(10, 0, False), nullable=False),
    Column('companydiscretionarydata', VARCHAR(20)),
    Column('companyentrydescription', VARCHAR(40)),
    Column('offsetaccountid', VARCHAR(64)),
    Column('numentries', NUMBER(10, 0, False)),
    Column('amount', NUMBER(38, 2, True)),
    Column('isprenote', VARCHAR(5)),
    Column('effectivedate', DateTime, nullable=False),
    Column('status', NUMBER(10, 0, False), nullable=False),
    Column('masteruserid', VARCHAR(10)),
    Column('dataspace', VARCHAR(10)),
    Column('initiatoruserid', VARCHAR(10)),
    Column('initiateddate', DateTime),
    Column('approveruserid', VARCHAR(10)),
    Column('approveddate', DateTime),
    Column('rejecteruserid', VARCHAR(10)),
    Column('rejecteddate', DateTime),
    Column('cancelleruserid', VARCHAR(10)),
    Column('cancelleddate', DateTime),
    Column('achbatchfileid', VARCHAR(10)),
    Column('businessname', VARCHAR(256)),
    Column('offsetaccountnumber', VARCHAR(40)),
    Column('offsetaccountnickname', VARCHAR(40)),
    Column('updateenterprisedate', DateTime, nullable=False),
    Column('recorddeleted', VARCHAR(5)),
    Column('isrestricted', VARCHAR(5)),
    Column('firstapproveruserid', VARCHAR(10)),
    Column('firstapproveddate', DateTime),
    Column('secondapproveruserid', VARCHAR(10)),
    Column('secondapproveddate', DateTime),
    Column('approvalsrequired', NUMBER(3, 0, False)),
    Column('issameday', VARCHAR(5)),
    Column('scheduleinfo', NUMBER(5, 0, False)),
    Column('updatecomment', Text),
    Column('offsetindividually', VARCHAR(5)),
    Column('achaccountnumber', VARCHAR(40)),
    Column('achtransactioncode', VARCHAR(10)),
    Column('prefundingstatus', NUMBER(5, 0, False)),
    Column('holdid', VARCHAR(50)),
    Column('alternateoffsetaccountnumber', VARCHAR(24)),
    Column('alternateoffsetaccounttype', NUMBER(3, 0, False)),
    Column('sweeptransactionid', VARCHAR(30)),
    Column('sweepreversaltransactionid', VARCHAR(30)),
    Column('useparticipantdistributions', VARCHAR(5)),
    schema='COCCDM'
)


t_bank_v_achbatchtemplate = Table(
    'bank_v_achbatchtemplate', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('batchname', VARCHAR(40)),
    Column('companyid', NUMBER(19, 0, False), nullable=False),
    Column('transactiontype', NUMBER(10, 0, False), nullable=False),
    Column('companydiscretionarydata', VARCHAR(20)),
    Column('companyentrydescription', VARCHAR(10)),
    Column('offsetaccountid', VARCHAR(64)),
    Column('numentries', NUMBER(10, 0, False)),
    Column('amount', NUMBER(38, 2, True)),
    Column('holdamount', NUMBER(38, 2, True)),
    Column('numprenotes', NUMBER(10, 0, False)),
    Column('effectivedate', DateTime),
    Column('masteruserid', VARCHAR(50)),
    Column('recorddeleted', VARCHAR(5)),
    Column('isrestricted', VARCHAR(5)),
    Column('insertdateutc', DateTime),
    Column('offsetindividually', VARCHAR(5)),
    Column('useparticipantdistributions', VARCHAR(5)),
    schema='COCCDM'
)


t_bank_v_user = Table(
    'bank_v_user', Base.metadata,
    Column('masteruserid', NUMBER(19, 0, False)),
    Column('businessuserid', NUMBER(19, 0, False)),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('institutionid', NUMBER(19, 0, False), nullable=False),
    Column('institutionuserid', VARCHAR(32)),
    Column('dataspace', VARCHAR(10)),
    Column('title', VARCHAR(32)),
    Column('firstname', VARCHAR(64)),
    Column('middlename', VARCHAR(64)),
    Column('lastname', VARCHAR(256)),
    Column('suffix', VARCHAR(32)),
    Column('birthdate', DateTime),
    Column('status', NUMBER(3, 0, False)),
    Column('primaryaddressid', NUMBER(19, 0, False)),
    Column('primaryemailid', NUMBER(19, 0, False)),
    Column('primaryphoneid', NUMBER(19, 0, False)),
    Column('recorddeleted', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('updatedateutc', DateTime, nullable=False),
    Column('updatingappname', VARCHAR(50)),
    Column('updatingprocname', VARCHAR(50)),
    Column('updatinguserid', VARCHAR(50)),
    Column('timezone', VARCHAR(50)),
    Column('preferredculture', VARCHAR(20)),
    Column('isadmin', VARCHAR(5)),
    schema='COCCDM'
)


t_bank_v_usersecurity = Table(
    'bank_v_usersecurity', Base.metadata,
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('institutionid', NUMBER(19, 0, False), nullable=False),
    Column('loginname', VARCHAR(101)),
    Column('passwordhash', VARCHAR(512)),
    Column('institutionuserid', VARCHAR(32)),
    Column('title', VARCHAR(32)),
    Column('firstname', VARCHAR(64)),
    Column('middlename', VARCHAR(64)),
    Column('lastname', VARCHAR(256)),
    Column('suffix', VARCHAR(32)),
    Column('birthdate', DateTime),
    Column('passwordexpirationdateutc', DateTime),
    Column('lastlogindateutc', DateTime),
    Column('lastloginfailuredateutc', DateTime),
    Column('consecutiveloginfailures', NUMBER(10, 0, False), nullable=False),
    Column('changepasswordrequired', VARCHAR(5)),
    Column('recorddeleted', VARCHAR(5)),
    Column('updatedateutc', DateTime, nullable=False),
    Column('timezone', VARCHAR(50)),
    Column('status', NUMBER(3, 0, False)),
    Column('changeloginnamecount', NUMBER(10, 0, False), nullable=False),
    Column('lastpasswordchangedatetimeutc', DateTime),
    Column('dataspace', VARCHAR(10)),
    Column('primaryaddressid', NUMBER(19, 0, False)),
    Column('primaryemailid', NUMBER(19, 0, False)),
    Column('primaryphoneid', NUMBER(19, 0, False)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('updatingappname', VARCHAR(50)),
    Column('updatingprocname', VARCHAR(50)),
    Column('updatinguserid', VARCHAR(50)),
    Column('preferredculture', VARCHAR(20)),
    schema='COCCDM'
)


t_bank_wireparticipant = Table(
    'bank_wireparticipant', Base.metadata,
    Column('routingnumber', VARCHAR(9)),
    Column('telegraphicname', VARCHAR(18)),
    Column('customername', VARCHAR(36)),
    Column('state', VARCHAR(2)),
    Column('city', VARCHAR(25)),
    Column('fundstransferstatus', VARCHAR(5)),
    Column('fundssettlementonlystatus', VARCHAR(5)),
    Column('bookentrysecuritiestransstat', VARCHAR(5)),
    Column('createdatetimeutc', DateTime, nullable=False),
    Column('updatedatetimeutc', DateTime),
    schema='COCCDM'
)


t_bank_wirepayeetemplate = Table(
    'bank_wirepayeetemplate', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('masteruserid', NUMBER(19, 0, False), nullable=False),
    Column('templatename', VARCHAR(100)),
    Column('beneficiaryname', VARCHAR(50)),
    Column('beneficiaryaccountnumber', VARCHAR(50)),
    Column('contactname', VARCHAR(100)),
    Column('contactphone', VARCHAR(50)),
    Column('contactfax', VARCHAR(50)),
    Column('wiretype', VARCHAR(50)),
    Column('beneficiaryaddressline1', VARCHAR(50)),
    Column('beneficiaryaddressline2', VARCHAR(50)),
    Column('beneficiarycity', VARCHAR(50)),
    Column('beneficiarystate', VARCHAR(50)),
    Column('beneficiarypostalcode', VARCHAR(50)),
    Column('beneficiarycountry', VARCHAR(50)),
    Column('beneficiaryfibanknumbertype', VARCHAR(50)),
    Column('beneficiaryfibanknumber', VARCHAR(50)),
    Column('beneficiaryfiname', VARCHAR(50)),
    Column('beneficiaryfiaddressline1', VARCHAR(50)),
    Column('beneficiaryfiaddressline2', VARCHAR(50)),
    Column('beneficiaryficity', VARCHAR(50)),
    Column('beneficiaryfistate', VARCHAR(50)),
    Column('beneficiaryfipostalcode', VARCHAR(50)),
    Column('beneficiaryficountry', VARCHAR(50)),
    Column('receivingfibanknumbertype', VARCHAR(50)),
    Column('receivingfibanknumber', VARCHAR(50)),
    Column('receivingfiname', VARCHAR(50)),
    Column('receivingfiaddressline1', VARCHAR(50)),
    Column('receivingfiaddressline2', VARCHAR(50)),
    Column('receivingficity', VARCHAR(50)),
    Column('receivingfistate', VARCHAR(50)),
    Column('receivingfipostalcode', VARCHAR(50)),
    Column('receivingficountry', VARCHAR(50)),
    Column('intermediaryfibanknumbertype', VARCHAR(50)),
    Column('intermediaryfibanknumber', VARCHAR(50)),
    Column('intermediaryfiname', VARCHAR(50)),
    Column('intermediaryfiaddressline1', VARCHAR(50)),
    Column('intermediaryfiaddressline2', VARCHAR(50)),
    Column('intermediaryficity', VARCHAR(50)),
    Column('intermediaryfistate', VARCHAR(50)),
    Column('intermediaryfipostalcode', VARCHAR(50)),
    Column('intermediaryficountry', VARCHAR(50)),
    Column('lastfundingaccountid', VARCHAR(64)),
    Column('lastmemo', VARCHAR(140)),
    Column('recorddeleted', VARCHAR(5)),
    Column('creatinguserid', NUMBER(19, 0, False)),
    Column('beneficiaryfiadvicecode', VARCHAR(3)),
    Column('beneficiaryfiadviceinfo', VARCHAR(191)),
    Column('intermediaryfiadvicecode', VARCHAR(3)),
    Column('intermediaryfiadviceinfo', VARCHAR(191)),
    Column('receivingfiadvicecode', VARCHAR(3)),
    Column('receivingfiadviceinfo', VARCHAR(191)),
    Column('beneficiaryemailaddress', VARCHAR(256)),
    Column('notifybeneficiarybydefault', VARCHAR(5)),
    schema='COCCDM'
)


t_bank_wiretransfer = Table(
    'bank_wiretransfer', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('masteruserid', NUMBER(19, 0, False), nullable=False),
    Column('initiatinguserid', NUMBER(19, 0, False), nullable=False),
    Column('firstapproveruserid', NUMBER(19, 0, False)),
    Column('secondapproveruserid', NUMBER(19, 0, False)),
    Column('status', VARCHAR(50)),
    Column('originatingtemplateid', NUMBER(19, 0, False)),
    Column('originatingtemplatename', VARCHAR(100)),
    Column('wiredate', DateTime, nullable=False),
    Column('fundingaccountid', VARCHAR(64)),
    Column('amount', NUMBER(18, 2, True), nullable=False),
    Column('memo', VARCHAR(140)),
    Column('beneficiaryname', VARCHAR(50)),
    Column('beneficiaryaccountnumber', VARCHAR(50)),
    Column('wiretype', VARCHAR(50)),
    Column('beneficiaryaddressline1', VARCHAR(50)),
    Column('beneficiaryaddressline2', VARCHAR(50)),
    Column('beneficiarycity', VARCHAR(50)),
    Column('beneficiarystate', VARCHAR(50)),
    Column('beneficiarypostalcode', VARCHAR(50)),
    Column('beneficiarycountry', VARCHAR(50)),
    Column('beneficiaryfibanknumbertype', VARCHAR(50)),
    Column('beneficiaryfibanknumber', VARCHAR(50)),
    Column('beneficiaryfiname', VARCHAR(50)),
    Column('beneficiaryfiaddressline1', VARCHAR(50)),
    Column('beneficiaryfiaddressline2', VARCHAR(50)),
    Column('beneficiaryficity', VARCHAR(50)),
    Column('beneficiaryfistate', VARCHAR(50)),
    Column('beneficiaryfipostalcode', VARCHAR(50)),
    Column('beneficiaryficountry', VARCHAR(50)),
    Column('receivingfibanknumbertype', VARCHAR(50)),
    Column('receivingfibanknumber', VARCHAR(50)),
    Column('receivingfiname', VARCHAR(50)),
    Column('receivingfiaddressline1', VARCHAR(50)),
    Column('receivingfiaddressline2', VARCHAR(50)),
    Column('receivingficity', VARCHAR(50)),
    Column('receivingfistate', VARCHAR(50)),
    Column('receivingfipostalcode', VARCHAR(50)),
    Column('receivingficountry', VARCHAR(50)),
    Column('intermediaryfibanknumbertype', VARCHAR(50)),
    Column('intermediaryfibanknumber', VARCHAR(50)),
    Column('intermediaryfiname', VARCHAR(50)),
    Column('intermediaryfiaddressline1', VARCHAR(50)),
    Column('intermediaryfiaddressline2', VARCHAR(50)),
    Column('intermediaryficity', VARCHAR(50)),
    Column('intermediaryfistate', VARCHAR(50)),
    Column('intermediaryfipostalcode', VARCHAR(50)),
    Column('intermediaryficountry', VARCHAR(50)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('updatedateutc', DateTime),
    Column('updatecomment', VARCHAR(250)),
    Column('fundingaccountnickname', VARCHAR(100)),
    Column('fundingaccountdescription', VARCHAR(100)),
    Column('fundinginstitutionacctnbr', VARCHAR(100)),
    Column('fundingmaskinstitutionacctnbr', VARCHAR(100)),
    Column('imad', VARCHAR(22)),
    Column('statuschangedbyuserid', NUMBER(19, 0, False)),
    Column('statuschangeddateutc', DateTime),
    Column('firstapproverapprovaldateutc', DateTime),
    Column('beneficiaryfiadvicecode', VARCHAR(3)),
    Column('beneficiaryfiadviceinfo', VARCHAR(191)),
    Column('intermediaryfiadvicecode', VARCHAR(3)),
    Column('intermediaryfiadviceinfo', VARCHAR(191)),
    Column('receivingfiadvicecode', VARCHAR(3)),
    Column('receivingfiadviceinfo', VARCHAR(191)),
    Column('secondapproverapprovaldateutc', DateTime),
    Column('approvalsrequired', NUMBER(3, 0, False)),
    Column('scheduleid', NUMBER(19, 0, False)),
    Column('beneficiaryemailaddress', VARCHAR(256)),
    Column('notifybeneficiary', VARCHAR(5)),
    Column('currencycode', VARCHAR(3)),
    schema='COCCDM'
)


t_bank_wiretransfer_wirebatch = Table(
    'bank_wiretransfer_wirebatch', Base.metadata,
    Column('wiretransferid', NUMBER(19, 0, False), nullable=False),
    Column('wirebatchid', NUMBER(19, 0, False), nullable=False),
    schema='COCCDM'
)


class Cardmemberissuehist(Base):
    __tablename__ = 'cardmemberissuehist'
    __table_args__ = (
        PrimaryKeyConstraint('agreenbr', 'membernbr', 'issuenbr', 'effdatetime', 'timeuniqueextn', name='pk_cardmemberissuehist'),
        {'schema': 'COCCDM'}
    )

    agreenbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    membernbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    issuenbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    effdatetime: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    timeuniqueextn: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    cardstatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    statreason: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    datesent: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    cardstatreasoncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))


t_disc_disclosure = Table(
    'disc_disclosure', Base.metadata,
    Column('disclosureid', NUMBER(19, 0, False), nullable=False),
    Column('name', VARCHAR(100)),
    Column('dataspace', VARCHAR(50)),
    Column('locationpageid', Text),
    Column('declinepageid', VARCHAR(50)),
    Column('priority', NUMBER(10, 0, False), nullable=False),
    Column('startdate', DateTime, nullable=False),
    Column('enddate', DateTime, nullable=False),
    Column('deletedate', DateTime),
    Column('isactive', VARCHAR(5)),
    schema='COCCDM'
)


t_disc_disclosureaccepthist = Table(
    'disc_disclosureaccepthist', Base.metadata,
    Column('accepteddisclosureid', NUMBER(19, 0, False), nullable=False),
    Column('userid', VARCHAR(50)),
    Column('disclosureid', NUMBER(19, 0, False), nullable=False),
    Column('disclosureversionid', NUMBER(19, 0, False), nullable=False),
    Column('actiondate', DateTime, nullable=False),
    Column('isaccepted', VARCHAR(5)),
    Column('isresetbyadmin', VARCHAR(5)),
    schema='COCCDM'
)


t_disc_disclosureaccepthist_temp = Table(
    'disc_disclosureaccepthist_temp', Base.metadata,
    Column('accepteddisclosureid', NUMBER(19, 0, False), nullable=False),
    Column('userid', VARCHAR(50)),
    Column('disclosureid', NUMBER(19, 0, False), nullable=False),
    Column('disclosureversionid', NUMBER(19, 0, False), nullable=False),
    Column('actiondate', DateTime, nullable=False),
    Column('isaccepted', VARCHAR(5)),
    Column('isresetbyadmin', VARCHAR(5)),
    schema='COCCDM'
)


t_disc_disclosureversion = Table(
    'disc_disclosureversion', Base.metadata,
    Column('disclosureversionid', NUMBER(19, 0, False), nullable=False),
    Column('disclosurelanguageid', NUMBER(19, 0, False), nullable=False),
    Column('disclosuretitle', VARCHAR(150)),
    Column('disclosurehtmlcontent', Text),
    Column('version', NUMBER(19, 0, False), nullable=False),
    schema='COCCDM'
)


t_dm_accountdisclosurehist = Table(
    'dm_accountdisclosurehist', Base.metadata,
    Column('user_id', VARCHAR(50)),
    Column('disclosure_id', VARCHAR(50)),
    Column('disclosure_accepted_datetime', DateTime, nullable=False),
    Column('disclosure_content', Text),
    schema='COCCDM'
)


t_dm_accountdisclosurehist_temp = Table(
    'dm_accountdisclosurehist_temp', Base.metadata,
    Column('user_id', VARCHAR(50)),
    Column('disclosure_id', VARCHAR(50)),
    Column('disclosure_accepted_datetime', DateTime, nullable=False),
    Column('disclosure_content', Text),
    schema='COCCDM'
)


class Docreq(Base):
    __tablename__ = 'docreq'
    __table_args__ = (
        PrimaryKeyConstraint('reqnbr', name='pk_docreq'),
        {'schema': 'COCCDM'}
    )

    reqnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    doctypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    freqcalpercd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    effdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    nextduedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    inactivedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    gracedays: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    followupdays: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    reqpersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    reqorgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    reftaxorgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    reftaxtypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    refacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    refpropnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    refintrpolicynbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    refliennbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    commenttext: Mapped[Optional[str]] = mapped_column(VARCHAR(256))
    followupdays2: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))


class Doctyp(Base):
    __tablename__ = 'doctyp'
    __table_args__ = (
        PrimaryKeyConstraint('doctypcd', name='pk_doctyp'),
        {'schema': 'COCCDM'}
    )

    doctypcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    doctypdesc: Mapped[str] = mapped_column(VARCHAR(30))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    verificationidyn: Mapped[str] = mapped_column(VARCHAR(1))
    docstoragemethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    freqcalpercd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    gracedays: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    followupdays: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    scanidyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    followupdays2: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    desctokennbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    descnamespacecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))


class Eagreepers(Base):
    __tablename__ = 'eagreepers'
    __table_args__ = (
        PrimaryKeyConstraint('agreenbr', 'persnbr', name='pk_eagreepers'),
        {'schema': 'COCCDM'}
    )

    agreenbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    persnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    currrev: Mapped[float] = mapped_column(NUMBER(22, 0, False))
    revdatetime: Mapped[datetime.datetime] = mapped_column(DateTime)
    revpersnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False))
    userid: Mapped[str] = mapped_column(VARCHAR(32))
    currpassword: Mapped[str] = mapped_column(VARCHAR(32))
    changepasswordonnextloginyn: Mapped[str] = mapped_column(CHAR(1))
    activeyn: Mapped[str] = mapped_column(CHAR(1))
    numfailedlogins: Mapped[float] = mapped_column(NUMBER(22, 0, False))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    oldpassword: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    useriddesc: Mapped[Optional[str]] = mapped_column(VARCHAR(50))


t_em_attachment = Table(
    'em_attachment', Base.metadata,
    Column('attachmentid', NUMBER(19, 0, False), nullable=False),
    Column('messageid', NUMBER(19, 0, False), nullable=False),
    Column('filename', VARCHAR(100)),
    Column('mimetype', VARCHAR(50)),
    Column('content', Text),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_em_broadcast = Table(
    'em_broadcast', Base.metadata,
    Column('broadcastid', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('subject', VARCHAR(500)),
    Column('body', Text),
    Column('startdateutc', DateTime, nullable=False),
    Column('enddateutc', DateTime),
    Column('authoruserid', NUMBER(19, 0, False), nullable=False),
    Column('categoryid', NUMBER(19, 0, False)),
    Column('priorityid', NUMBER(19, 0, False), nullable=False),
    Column('allowreply', VARCHAR(5)),
    Column('active', VARCHAR(5)),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    Column('targetkey', VARCHAR(128)),
    schema='COCCDM'
)


t_em_broadcastactivity = Table(
    'em_broadcastactivity', Base.metadata,
    Column('broadcastactivityid', NUMBER(19, 0, False), nullable=False),
    Column('broadcastid', NUMBER(19, 0, False), nullable=False),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('activity', VARCHAR(100)),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_em_broadcastactivity_temp = Table(
    'em_broadcastactivity_temp', Base.metadata,
    Column('broadcastactivityid', NUMBER(19, 0, False), nullable=False),
    Column('broadcastid', NUMBER(19, 0, False), nullable=False),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('activity', VARCHAR(100)),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_em_broadcasttarget = Table(
    'em_broadcasttarget', Base.metadata,
    Column('broadcasttargetid', NUMBER(19, 0, False), nullable=False),
    Column('broadcastid', NUMBER(19, 0, False), nullable=False),
    Column('targetvalue', VARCHAR(128)),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_em_category = Table(
    'em_category', Base.metadata,
    Column('categoryid', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('name', VARCHAR(255)),
    Column('description', VARCHAR(500)),
    Column('isarchived', VARCHAR(5)),
    Column('initialqueueid', NUMBER(19, 0, False), nullable=False),
    Column('initialpriorityid', NUMBER(19, 0, False), nullable=False),
    Column('isenduserselectable', VARCHAR(5)),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_em_extendedthreaddata = Table(
    'em_extendedthreaddata', Base.metadata,
    Column('extendedthreaddataid', NUMBER(19, 0, False), nullable=False),
    Column('extendedthreaddatafieldid', NUMBER(10, 0, False), nullable=False),
    Column('threadid', NUMBER(19, 0, False), nullable=False),
    Column('integervalue', NUMBER(19, 0, False)),
    Column('stringvalue', VARCHAR(512)),
    Column('datetimevalue', DateTime),
    Column('floatvalue', Double),
    Column('moneyvalue', NUMBER(19, 4, True)),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_em_extendedthreaddatafield = Table(
    'em_extendedthreaddatafield', Base.metadata,
    Column('extendedthreaddatafieldid', NUMBER(10, 0, False), nullable=False),
    Column('name', VARCHAR(64)),
    Column('description', VARCHAR(256)),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_em_message = Table(
    'em_message', Base.metadata,
    Column('messageid', NUMBER(19, 0, False), nullable=False),
    Column('body', Text),
    Column('details', Text),
    Column('sentdatetimeutc', DateTime, nullable=False),
    Column('threadid', NUMBER(19, 0, False), nullable=False),
    Column('authoruserid', NUMBER(19, 0, False)),
    Column('iscreatedbyenduser', VARCHAR(5)),
    Column('isrecalled', VARCHAR(5)),
    Column('isread', VARCHAR(5)),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_em_priority = Table(
    'em_priority', Base.metadata,
    Column('priorityid', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('name', VARCHAR(100)),
    Column('description', VARCHAR(500)),
    Column('numericalvalue', NUMBER(10, 0, False), nullable=False),
    Column('isarchived', VARCHAR(5)),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_em_queue = Table(
    'em_queue', Base.metadata,
    Column('queueid', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('name', VARCHAR(100)),
    Column('description', VARCHAR(500)),
    Column('isarchived', VARCHAR(5)),
    Column('notifyemail', VARCHAR(100)),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_em_standardresponse = Table(
    'em_standardresponse', Base.metadata,
    Column('standardresponseid', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('name', VARCHAR(300)),
    Column('response', Text),
    Column('ordernumber', NUMBER(10, 0, False), nullable=False),
    Column('categoryid', NUMBER(19, 0, False)),
    Column('isglobal', VARCHAR(5)),
    Column('isarchived', VARCHAR(5)),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    Column('active', VARCHAR(5)),
    schema='COCCDM'
)


t_em_status = Table(
    'em_status', Base.metadata,
    Column('statusid', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('name', VARCHAR(255)),
    Column('description', VARCHAR(500)),
    Column('isarchived', VARCHAR(5)),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_em_thread = Table(
    'em_thread', Base.metadata,
    Column('threadid', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('subject', VARCHAR(500)),
    Column('owneruserid', NUMBER(19, 0, False)),
    Column('enduserid', NUMBER(19, 0, False)),
    Column('categoryid', NUMBER(19, 0, False), nullable=False),
    Column('queueid', NUMBER(19, 0, False), nullable=False),
    Column('priorityid', NUMBER(19, 0, False), nullable=False),
    Column('statusid', NUMBER(19, 0, False), nullable=False),
    Column('broadcastid', NUMBER(19, 0, False)),
    Column('statusdateutc', DateTime, nullable=False),
    Column('notes', Text),
    Column('trackingid', VARCHAR(16)),
    Column('allowreply', VARCHAR(5)),
    Column('isarchivedbycsr', VARCHAR(5)),
    Column('isarchivedbyenduser', VARCHAR(5)),
    Column('isrecalled', VARCHAR(5)),
    Column('alertonresponse', VARCHAR(5)),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    Column('isalertsent', VARCHAR(5)),
    schema='COCCDM'
)


t_em_threadchangehistory = Table(
    'em_threadchangehistory', Base.metadata,
    Column('threadchangehistoryid', NUMBER(19, 0, False), nullable=False),
    Column('threadid', NUMBER(19, 0, False), nullable=False),
    Column('editoruserid', NUMBER(19, 0, False)),
    Column('details', Text),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_em_threadchangehistory_temp = Table(
    'em_threadchangehistory_temp', Base.metadata,
    Column('threadchangehistoryid', NUMBER(19, 0, False), nullable=False),
    Column('threadid', NUMBER(19, 0, False), nullable=False),
    Column('editoruserid', NUMBER(19, 0, False)),
    Column('details', Text),
    Column('insertdatetimeutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('lastupdatingdatetimeutc', DateTime, nullable=False),
    Column('lastupdatingappname', VARCHAR(50)),
    Column('lastupdatingprocname', VARCHAR(50)),
    Column('lastupdatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


class Encapplications(Base):
    __tablename__ = 'encapplications'
    __table_args__ = (
        PrimaryKeyConstraint('encompassid', 'applicationid', 'applicationindex', name='encapplications_pk'),
        {'schema': 'COCCDM'}
    )

    encompassid: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    applicationid: Mapped[str] = mapped_column(VARCHAR(100), primary_key=True)
    applicationindex: Mapped[int] = mapped_column(Integer, primary_key=True)
    borrower_fnamewmiddlename_36: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    borrower_lastnamewsuffix_37: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    borrower_ageatapplication_38: Mapped[Optional[int]] = mapped_column(Integer)
    borrower_maritalstatustyp_52: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    coborr_expcrdtscor_60: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_taxid_65: Mapped[Optional[str]] = mapped_column(VARCHAR(11))
    borr_homephonenum_66: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    borr_experiancreditscore_67: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    coborrower_fnamewithmname_68: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    coborrower_lnamewithsuffix_69: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    coborrower_ageatappyearscnt_70: Mapped[Optional[int]] = mapped_column(Integer)
    coborrower_maritalstatustyp_84: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    coborrower__taxid_97: Mapped[Optional[str]] = mapped_column(VARCHAR(11))
    borrower_hmdarefusalind_188: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrower_hmdarefusalind_189: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    creditreportreferenceid_300: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    borrower_hmdagendertyp_471: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    coborrower_hmdagendertyp_478: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    totalincomeamount_736: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    topratiopercent_740: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bottomratiopercent_742: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borrower_emailaddresstext_1240: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    totalgrossmnthlyincomeamt_1389: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borrower_birthdate_1402: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    coborrower_birthdate_1403: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    borrower_equifaxscore_1414: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    coborrower_equifaxscore_1415: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    borrower_transunionscore_1450: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    coborrow_transunionscore_1452: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    borrower_minficoscore_1484: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    coborrower_minficoscore_1502: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    borrower_hmdaethnicitytyp_1523: Mapped[Optional[str]] = mapped_column(VARCHAR(24))
    borrower_hmdaameindianind_1524: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_hmdaasianind_1525: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_hmdaafriameind_1526: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_hmdapacislandind_1527: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_hmdawhiteind_1528: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_hmdanotprovidind_1529: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_hmdanotappliind_1530: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrow_hmdaethnicitytyp_1531: Mapped[Optional[str]] = mapped_column(VARCHAR(24))
    coborrow_hmdaameriindiind_1532: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrow_hmdaasianind_1533: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrow_hmdaafriameriind_1534: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrow_hmdapacislandind_1535: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrow_hmdawhiteind_1536: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrow_hmdanotprovind_1537: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrow_hmdanotapplind_1538: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    propertyusagetyp_1811: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    borrower_middleficoscore_2849: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    coborrow_middleficoscore_2850: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrower_nocoappliind_3174: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrow_4506ttlyrvarijnt1_3329: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borrow_4506yrlyvarijnt2_3330: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    coborrow_hmdanocoappliind_3840: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_firstname_4000: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    borrower_middlename_4001: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    borrower_lastname_4002: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    borrower_suffixtoname_4003: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    coborrower_firstname_4004: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    coborrower_middlename_4005: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    coborrower_lastname_4006: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    coborrower_suffixtoname_4007: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    borrow_ethnicitybasvisual_4121: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    borrow_racebasevisual_4122: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    borrow_sexbasevisual_4123: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    borrow_otherhisplatinori_4125: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    borrow_ameriindiantribe_4126: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    borrow_otherasianrace_4128: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    borr_otherpaciislandrace_4130: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    coborrow_applicmethodtyp_4131: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    coborr_ethnicbasedonvis_4132: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    coborr_racebasedonvisual_4133: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    coborrow_sexbasedonvisual_4134: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    coborr_othrhispanlatino_4136: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    coborrow_ameriindiantribe_4137: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    coborrow_otherasianrace_4139: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    coborr_othrpaciislandrace_4141: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    borr_applitakenmethodtyp_4143: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    borrow_mexicanind_4144: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrow_puertoricanind_4145: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrow_cubanind_4146: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_hisplatothrorigind_4147: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrow_hmdaasianindianind_4148: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_hmdachineseind_4149: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_hmdafilipinoind_4150: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_hmdajapaneseind_4151: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_hmdakoreanind_4152: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrow_hmdavietnameseind_4153: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrow_hmdaasiaothraceind_4154: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrow_hmdanativhawaiind_4155: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrow_guamorchamorroind_4156: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_hmdasamoanind_4157: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrow_paciislandotherind_4158: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrower_hmdamexicanind_4159: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrow_hmdaprind_4160: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrower_hmdacubanind_4161: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_hisplatothrorigind_4162: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrow_hmdaasianindiind_4163: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrower_hmdachinese_4164: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_filipino_4165: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_japanese_4166: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_korean_4167: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_vietnamese_4168: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_asianotherrace_4169: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_nativehawaiian_4170: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_guamanianorchamorro_4171: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_samoan_4172: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_pacislandother_4173: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_creditscorefordecimak_4174: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    bor_creditscoringmodel_4175: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    bor_otherscoringmodel_4176: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    cobor_crdtscrfordecimak_4177: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    cobor_creditscoringmodel_4178: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    cobor_otherscoringmodel_4179: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    bor_age_4183: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    cobor_age_4184: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    cobor_nocoapplethnicity_4188: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_nocoapplicantsex_4189: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_gendertypfemale_4193: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_gendertypmale_4194: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_gendertypdonotwish_4195: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_gendertypnotappl_4196: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_gendertypfemale_4197: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_gendertypmale_4198: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_gndtypnowish_4199: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_gendertypnotappl_4200: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_ethnicitydonotwish_4205: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_ethnicitydonotwish_4206: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_ethnhisplat_4210: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_ethnothispaniclatino_4211: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_ethnotapplicable_4212: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_ethnotapplicableind_4215: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_racerptfield1_4216: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    bor_racerptfield2_4217: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    bor_racerptfield3_4218: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    bor_racerptfield4_4219: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    bor_racerptfield5_4220: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    bor_ethrptfield1_4221: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    bor_ethrptfield2_4222: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    bor_ethrptfield3_4223: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    borr_ethreportedfield4_4224: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    borr_ethreportedfield5_4225: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    coborr_racereportedfield1_4226: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    coborr_racereportedfield2_4227: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    coborr_racereportedfield3_4288: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    coborr_racereportedfield4_4229: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    cobor_racerptfield5_4230: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    coborr_ethreportedfield1_4231: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    coborr_ethreportedfield2_4232: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    coborr_ethreportedfield3_4233: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    coborr_ethreportedfield4_4234: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    coborr_ethreportedfield5_4235: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    bor_ethninfonotprov_4243: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_raceinfonotprovided_4244: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_sexinfonotprovided_4245: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_ethinfonotprovided_4246: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_raceinfonotprov_4247: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_sexinfonotprov_4248: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    grossotherincomeamt_1168: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_experian30days_2324: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_experian60days_2325: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_experian90days_2326: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_experian120days_2327: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_transunion30days_2328: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_transunion60days_2329: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_transunion90days_2330: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_transunion120days_2331: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_equifax30days_2332: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_equifax60days_2333: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_equifax90days_2334: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_equifax120days_2335: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borrower_creditrcvddate_2336: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    borrower_priorforeclosure_2339: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_dateofbankruptcy_2340: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    bor_dateofforeclosure_2341: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    bor_experian150days_2555: Mapped[Optional[int]] = mapped_column(Integer)
    bor_transunion150days_2556: Mapped[Optional[int]] = mapped_column(Integer)
    bor_equifax150days_2557: Mapped[Optional[int]] = mapped_column(Integer)
    borrower_pass30days_2558: Mapped[Optional[int]] = mapped_column(Integer)
    borrower_pass60days_2559: Mapped[Optional[int]] = mapped_column(Integer)
    borrower_pass90days_2560: Mapped[Optional[int]] = mapped_column(Integer)
    borrower_pass120days_2561: Mapped[Optional[int]] = mapped_column(Integer)
    borrower_pass150days_2562: Mapped[Optional[int]] = mapped_column(Integer)
    borrower_mortgageoncredit_2563: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_numberoftradelines_2564: Mapped[Optional[int]] = mapped_column(Integer)
    borr_yearsofcreditonfile_2565: Mapped[Optional[int]] = mapped_column(Integer)
    borrower_creditcounseling_2566: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrow_highestcreditlimit_2567: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borrower_openbankruptcy2_2568: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borrower_priorbankruptcy2_2569: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    borrower_bankruptcystatus_2570: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borr_foreclosuresatisfied_2571: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    borr_foreclosurestatus_2572: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    totalmonthlypaymentamount_350: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    coborr_authcrdtrptind_4076: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_dateauthcredrpt_4077: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    coborr_creditrptauthmeth_4078: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borrower_workphonenumber_4533: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    coborr_workphonenumber_4534: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    totalassetsamount_732: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borr_totalliabbalamt_733: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    networthamount_734: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borr_totalpreshousexpamt_737: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borr_subliqasstsmingftamt_915: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    reototalmarketvalueamount_919: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    reoproperties_owner0_fm0046: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    reoproperties_unittyp0_fm0047: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    reprop_unitnumber0_fm0048: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    reprop_liabdonotapply0_fm0049: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    reprop_urla2020stadd0_fm0050: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    reoproperties_owner1_fm0146: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    reoproperties_unittyp1_fm0147: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    reprop_unitnumber1_fm0148: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    reprop_liabdonotapply1_fm0149: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    reprop_urla2020stadd1_fm0150: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borr_2credscrfordecmak_x116: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borr_2creditscoringmodel_x117: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    coborr_2crdtscrfordecimak_x118: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    coborr_2creditscormodel_x119: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borr_urla2020citirestyp_urlax1: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borr_partytolawsuit_urlax100: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_partytolawsuit_urlax101: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_priprodeedlieucon_urlax102: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_priprodeelicon_urlax103: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_priproshrtsaecmpl_urlax104: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_priorproshtsle_urlax105: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_pripropclsurcmp_urlax106: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_pripropclsurcmp_urlax107: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_realestdonotapp_urlax110: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_legalotherthansp_urlax111: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_lglothrthansp_urlax1112: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_domrshiptyp_urlax113: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    coborr_domrshiptyp_urlax114: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borr_othrrshiptypdesc_urlax115: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    cobor_othrrshptypdesc_urlax116: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    borrower_state_urlax117: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    coborrower_stateurlax118: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    borr_prtonaddborrpage_urlax121: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_prtonaddborrpg_urlax122: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_activeduty_urlax123: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrower_veteran_urlax124: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_resenatgrdresact_urlax125: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrower_activeduty_urlax126: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborrower_veteran_urlax127: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_resnagrdresac_urlax128: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_selfdeclarmilser_urlax13: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_selfdeclmilser_urlax14: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_ownershipconfirm_urlax153: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_ownrshpfrmttyp_urlax154: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borr_oshippartyrole_urlax155: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    coborr_oshipconf_urlax159: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_oshipformattyp_urlax160: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    coborr_oshippartyrole_urlax161: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borr_militaserexpcom_urlax17: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    borr_bruptchapseven_urlax174: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_bruptchapeleven_urlax175: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_bruptchaptwelve_urlax176: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_bruptchapthrtn_urlax177: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_bruptchapseven_urlax178: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_bruptchapele_urlax179: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_milityserexpect_urlax18: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    coborr_bruptchaptwlve_urlax180: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_bruptchapthrtn_urlax181: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_spousalvabeneelig_urlax19: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_urlaaliasname_urlax195: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    coborr_urlaaliasname_urlax196: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borr_currempnoapply_urlax199: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_urla2020citresi_urlax2: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    coborr_spsalvabeneelig_urlax20: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_currempnoapply_urlax200: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_addempnoapply_urlax201: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_addempnoapply_urlax202: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_prevempnoapply_urlax203: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coborr_prevempnoapply_urlax204: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_langpreference_urlax21: Mapped[Optional[str]] = mapped_column(VARCHAR(24))
    borr_addinformation_urlax213: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    coborr_addinformation_urlax214: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    coborr_langpreference_urlax22: Mapped[Optional[str]] = mapped_column(VARCHAR(24))
    totaladdloansamount_urlax229: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    ttlapptodownpay_urlax230: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borr_jntassetliabrpt1_urlax234: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    borr_langcodeotherdesc_urlax35: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    coborr_langcdotrdesc_urlax36: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    borr_otrsrcincnoapply_urlax40: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_otrsrcincnoapply_urlax41: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borr_addotherinc_urlax42: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    coborr_addotherinc_urlax43: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    othertotalincome_urlax44: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    ttlurla2020assetsamt_urlax50: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borr_othrassetsnoapply_urlax51: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_othrasstsnoapply_urlax52: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    totalotherassetsamount_urlax54: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borrower_totalassets_urlax55: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    coborrower_totalassets_urlax56: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_totalotherassets_urlax57: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    cobor_totalotherassets_urlax58: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_liabnoapply_urlax59: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_liabnoapply_urlax60: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_totalliabamount_urlax62: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_otherliabnoapply_urlax63: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_otherliabnoapply_urlax64: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_totalotherliab_urlax65: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    cobor_totalotherliab_urlax66: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_totalotherliabamt_urlax68: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_realestatenoapply_urlax69: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_giftsandgrantsbor_urlax82: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_giftsgrantsbor_urlax83: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_spclborsellerrship_urlax84: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_spclborsellerrel_urlax85: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_undisborowedfunds_urlax86: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_undisborfunds_urlax87: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_undisborfundsamt_urlax88: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    cobor_undisborfundsamt_urlax89: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bor_undismortgageapp_urlax90: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_undismortgageapp_urlax91: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_undiscreditapp_urlax92: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_undiscreditapp_urlax93: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_propcleanenrgylien_urlax94: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_propclnenrgylien_urlax95: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_undiscomakerofnote_urlax96: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_undiscomakerofnt_urlax97: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    bor_presentlydelurla_urlax98: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cobor_presentlydelurla_urlax99: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    owner0_urlargg0002: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    giftorgrantdate0_urlargg0003: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    printattachment0_urlargg0004: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    holdername0_urlargg0005: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    attention0_urlargg0006: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddstline0_urlargg0007: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddresscity0_urlargg0008: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddst0_urlargg0009: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    holderaddpostcode0_urlargg0010: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    holderphone0_urlargg0011: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    holderfax0_urlargg0012: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    holderemail0_urlargg0013: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    title0_urlargg0014: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    printusername0_urlargg0015: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    titlephone0_urlargg0016: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    titlefax0_urlargg0017: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    assettyp0_urlargg0018: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    source0_urlargg0019: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    deposited0_urlargg0020: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    amount0_urlargg0021: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    othersourcedesc0_urlargg0022: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    printuserjobttle1_urlargg0064: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    owner1_urlargg0102: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    giftorgrantdate1_urlargg0103: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    printattachment_urlargg0104: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    holdername1_urlargg0105: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    attention1_urlargg0106: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddstline11_urlargg0107: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddresscity1_urlargg0108: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddst1_urlargg0109: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    holderaddpostcode1_urlargg0110: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    holderphone1_urlargg0111: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    holderfax1_urlargg0112: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    holderemail1_urlargg0113: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    title1_urlargg0114: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    printusername_urlargg0115: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    titlephone1_urlargg0116: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    titlefax1_urlargg0117: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    assettyp1_urlargg0118: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    source1_urlargg0119: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    deposited_urlargg0120: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    amount1_urlargg0121: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    othersourcedesc1_urlargg0122: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    printuserjobttle1_urlargg0164: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrtyp0_urlaroa0001: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    assettyp0_urlaroa0002: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    cashormarketvalue0_urlaroa0003: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    otherdesc0_urlaroa0004: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holdername0_urlaroa005: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    attention0_urlaroa006: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddrstline0_urlaroa0007: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddresscity0_urlaroa0008: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddst0_urlaroa0009: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    holderaddrpostcd0_urlaroa0010: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    holderphone0_urlaroa0011: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    holderfax0_urlaroa0012: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    holderemail0_urlaroa0013: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otherassets_ttle0_urlaroa0014: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    printusername0_urlaroa0015: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    ttlephone0_urlaroa0016: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    ttlefax0_urlaroa0017: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    printattachment0_urlaroa0018: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    otherassetdate0_urlaroa0019: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    printuserjobttle0_urlaroa0020: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrtyp1_urlaroa0101: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    assettyp1_urlaroa0102: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    cashormarketvalue1_urlaroa0103: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    otherdesc1_urlaroa0104: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holdername1_urlaroa105: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    attention1_urlaroa106: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddrstline11_urlaroa0107: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddresscity1_urlaroa0108: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddst_urlaroa0109: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    holderaddrpostcd_urlaroa0110: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    holderphone1_urlaroa0111: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    holderfax1_urlaroa0112: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    holderemail1_urlaroa0113: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otherassets_ttle1_urlaroa0114: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    printusername1_urlaroa0115: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    ttlephone1_urlaroa0116: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    ttlefax1_urlaroa0117: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    printattachment1_urlaroa0118: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    otherassetdate1_urlaroa0119: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    printuserjobttle1_urlaroa0120: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    owner0_urlarois0002: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otherincsource0_urlarois0003: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    printattachment0_urlarois0004: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    holdername0_urlarois0005: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    attention0_urlarois0006: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddstline0_urlarois0007: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddcity0_urlarois0008: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddst0__urlarois0009: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    holderaddposcode0_urlarois0010: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    holderphone0_urlarois0011: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    holderfax0_urlarois0012: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    holderemail0_urlarois0013: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ttle0_urlarois0014: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    printusername0_urlarois0015: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    ttlephone0_urlarois0016: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    ttlefax0_urlarois0017: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    desc0_urlarois0018: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otherdesc0_urlarois0019: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    foreigninc0_urlarois0020: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    seasonalinc0_urlarois0021: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    monthlyamount0_urlarois0022: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    printuserjobttle0_urlarois0064: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    owner1_urlarois0102: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otherincsource_urlarois0103: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    printattachment1_urlarois0104: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    holdername1_urlarois0105: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    attention1_urlarois0106: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddstline11_urlarois0107: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddcity1_urlarois0108: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddst__urlarois0109: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    holderaddposcode_urlarois0110: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    holderphone1_urlarois0111: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    holderfax1_urlarois0112: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    holderemail1_urlarois0113: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ttle1_urlarois0114: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    printusername1_urlarois0115: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    ttlephone1_urlarois0116: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    ttlefax1_urlarois0117: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    desc1_urlarois0118: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otherdesc1_urlarois0119: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    foreigninc1_urlarois0120: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    seasonalinc1_urlarois0121: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    monthlyamount1_urlarois0122: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    printuserjobttle1_urlarois0164: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    otrliab_borrtyp_urlarol0001: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otrlia_liaorexptyp_urlarol0002: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otrliab_monthpay_urlarol0003: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    otrliab_otherdescr_urlarol0004: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otrliab_holderna_urlarol0005: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otherliab_attent_urlarol0006: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    othrliab_holdaddst_urlarol0007: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    othliab_hldaddcity_urlarol0008: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    othliab_holdaddst_urlarol0009: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    othli_hldaddposcod_urlarol0010: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    otherlia_holdphn_urlarol0011: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    otherliab_hldfax_urlarol0012: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    othliabi_holdeml_urlarol0013: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otherliabi_title_urlarol0014: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    othli_prtusrnmind_urlarol0015: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    othliab_titlephne_urlarol0016: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    othliab_titlefax_urlarol0017: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    othliab_prtattind_urlarol0018: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    otherliab_mthslft_urlarol0019: Mapped[Optional[int]] = mapped_column(Integer)
    otherliab_balance_urlarol0020: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    otherliab_credlim_urlarol0021: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    otherliab_depreq_urlarol0098: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    otrliab_borrtyp1__urlarol0101: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otrlia_liaorexptyp_urlarol0102: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otrliab_monthpay_urlarol0103: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    otrliab_otherdescr_urlarol0104: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otrliab_holderna_urlarol0105: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otherliab_attent_urlarol0106: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    othrliab_holdaddst_urlarol0107: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    othliab_hldaddcity_urlarol0108: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    othliab_holdaddst1_urlarol0109: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    othli_hldaddposcod_urlarol0110: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    otherlia_holdphn1_urlarol0111: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    otherliab_hldfax1_urlarol0112: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    othliabi_holdeml1_urlarol0113: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otherliabi_title1_urlarol0114: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    othli_prtusrnmind1_urlarol0115: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    othliab_titlephne1_urlarol0116: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    othliab_titlefax1_urlarol0117: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    othliab_prtattind1_urlarol0118: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    otherliab_mthslft1_urlarol0119: Mapped[Optional[int]] = mapped_column(Integer)
    otherliab_balance1_urlarol0120: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    otherliab_credlim1_urlarol0121: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    otherliab_depreq1_urlarol0198: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    urlacashmarkvalamt0_dd0048: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    urlacashmarkvalamt1_dd0148: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borrowertype0_urlaral0001: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holdername0_urlaral0002: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    attention0_urlaral0003: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddst0_urlaral0004: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddcity0_urlaral0005: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddst0_urlaral0006: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddpostcd0_urlaral0007: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderphone0_uralral0008: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderfax0_urlaral0009: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderemail0_urlaral0010: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    title0_urlaral0011: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    printusername0_urlaral0012: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    titlephone0_urlaral0013: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    titlefax0_urlara0014: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    printattachind0_urlaral0015: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    accounttype0_uraral0016: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    lienposition0_urlaral0017: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    monthlyprinint0_0urlaral0018: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    maxprinint5years0_urlaral0019: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    heloccrdtlimamt0_urlaral0020: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    helocinitdraw0_uralaral0021: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    amtappliedtodown0_urlaral0022: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    deffirstfiveyears0_urlaral0023: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    affordableloan0_urlaral0024: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    linkedpiggyback0_urlaral0025: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    indicreditor0_urlaral0032: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    printuserjobttl0_urlaral0064: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    addloanreqdate0_urlaral0098: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    borrowertype1_urlaral0101: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holdername1_urlaral0102: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    attention1_urlaral0103: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddst11_urlaral0104: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddcity_urlaral0105: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddst_urlaral0106: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderaddpostcd_urlaral0107: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderphone1_urlaral0108: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderfax1_urlaral0109: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    holderemail1_urlaral0110: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    title1_urlaral0111: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    printusername_urlaral0112: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    titlephone1_urlaral0113: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    titlefax1_urlaral0114: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    printattach_urlaral0115: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    accounttype1_urlaral0116: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    lienposition1_urlaral0117: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    monthlyprinandint_urlaral0118: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    maxprinint5years_urlaral0119: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    heloccrdtlimitamt_urlaral0120: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    helocinitialdraw1_urlaral0121: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    amtapptodwnpay1_urlaral0122: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    paydeffrstfiveyr_urlaral0123: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    affordableloan1_urlaral0124: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    linkedpiggyback_urlaral0125: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    indicreditor_urlaral0132: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    printuserjobtitle_urlaral0164: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    additionalloanreq_urlaral0198: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('SYSDATE'))


class Enccontacts(Base):
    __tablename__ = 'enccontacts'
    __table_args__ = (
        PrimaryKeyConstraint('encompassid', 'contactid', name='enccontacts_pk'),
        {'schema': 'COCCDM'}
    )

    encompassid: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    contactid: Mapped[str] = mapped_column(VARCHAR(50), primary_key=True)
    contactname: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    contacttype: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    name: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    phone: Mapped[Optional[str]] = mapped_column(VARCHAR(15))
    address: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    city: Mapped[Optional[str]] = mapped_column(VARCHAR(22))
    state: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    postalcode: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    contact: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    fhalenderid: Mapped[Optional[str]] = mapped_column(VARCHAR(12))
    investorname1: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    investorgrade1: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    investorscore1: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    investorname2: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    investorgrade2: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    investorscore2: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    investorname3: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    investorgrade3: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    investorscore3: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    insurancecertnumber: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    insdeterminationnumber: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    insdeterminationdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    insurancefloodzone: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    insurancemap: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    insurancenoofbedrooms: Mapped[Optional[int]] = mapped_column(Integer)
    loginid: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    referencenumber: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('SYSDATE'))


class Enccustomfields(Base):
    __tablename__ = 'enccustomfields'
    __table_args__ = (
        PrimaryKeyConstraint('encompassid', 'customfieldid', name='enccustomfields_pk'),
        {'schema': 'COCCDM'}
    )

    encompassid: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    customfieldid: Mapped[str] = mapped_column(VARCHAR(50), primary_key=True)
    fieldname: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    value: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('SYSDATE'))


class Encemployment(Base):
    __tablename__ = 'encemployment'
    __table_args__ = (
        PrimaryKeyConstraint('encompassid', 'applicationid', 'employid', name='encemployment_pk'),
        {'schema': 'COCCDM'}
    )

    encompassid: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    applicationid: Mapped[str] = mapped_column(VARCHAR(100), primary_key=True)
    employid: Mapped[str] = mapped_column(VARCHAR(50), primary_key=True)
    empname: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    monthlyincamt: Mapped[Optional[int]] = mapped_column(Integer)
    phonenumber: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    basepayamt: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    overtimeamt: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bonusamt: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    commissionsamt: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    otheramt: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    employstartdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    jobtermmonths: Mapped[Optional[int]] = mapped_column(Integer)
    militaryentitle: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    specialemprel: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    unittyp: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    unitnumber: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    urla2020stadd: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ownershipinttyp: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    employmonincamt: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    empname_1: Mapped[Optional[str]] = mapped_column(VARCHAR(22))
    addcity_1: Mapped[Optional[str]] = mapped_column(VARCHAR(22))
    addressstreetline1_1: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    addstate_1: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    addpostalcode_1: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    positiondescription_1: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    monthlyincamt_1: Mapped[Optional[int]] = mapped_column(Integer)
    selfemployed_1: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    phonenumber_1: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    basepayamt_1: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    commissionsamt_1: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    otheramt_1: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    employstartdate_1: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    jobtermmonths_1: Mapped[Optional[int]] = mapped_column(Integer)
    militaryentitlement_1: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    ownershipinttyp_1: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    employmonthlyincamt_1: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    unittyp_1: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    unitnumber_1: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    urla2020streetadd_1: Mapped[Optional[str]] = mapped_column(VARCHAR(22))
    timeinlineofworkyears_1: Mapped[Optional[int]] = mapped_column(Integer)
    overtimeamt_1: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    bonusamt_1: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    specialemprel_1: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    addressstreetline1: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    addcity: Mapped[Optional[str]] = mapped_column(VARCHAR(22))
    addstate: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    addpostalcode: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    enddate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    selfemployed: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    positiondescription: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    owner: Mapped[Optional[str]] = mapped_column(VARCHAR(15))
    currentemploymentind: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    timeinlineofworkyears: Mapped[Optional[int]] = mapped_column(Integer)
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('SYSDATE'))


class Encfees(Base):
    __tablename__ = 'encfees'
    __table_args__ = (
        PrimaryKeyConstraint('encompassid', 'feeid', name='encfees_pk'),
        {'schema': 'COCCDM'}
    )

    encompassid: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    feeid: Mapped[str] = mapped_column(VARCHAR(50), primary_key=True)
    feetype: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    borpaidamount: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    sellerpaidamount: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    monthlypayment: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    paidtoname: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    percentage: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    description: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    paidtoothers: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    ptb: Mapped[Optional[str]] = mapped_column(VARCHAR(8))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('SYSDATE'))


class Encgfe210fees(Base):
    __tablename__ = 'encgfe210fees'
    __table_args__ = (
        PrimaryKeyConstraint('encompassid', 'feeid', name='encgfe210fees_pk'),
        {'schema': 'COCCDM'}
    )

    encompassid: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    feeid: Mapped[str] = mapped_column(VARCHAR(50), primary_key=True)
    gfe2010feeparenttype: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    gfe2010feetype: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    gfe2010feeindex: Mapped[Optional[int]] = mapped_column(Integer)
    borpaidamount: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    ptbtype: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    amount: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    selpaidamount: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    amountdescription: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    rate: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    uselocompensationtoolind: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    paidbytype: Mapped[Optional[str]] = mapped_column(VARCHAR(6))
    section800chargeamount: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    hud1p2ttlstlmtchrgs: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    loanbalriseind: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    section800selchargeamount: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    totalofinitialfees: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('SYSDATE'))


class Encincome(Base):
    __tablename__ = 'encincome'
    __table_args__ = (
        PrimaryKeyConstraint('encompassid', 'applicationid', 'incomeid', name='encincome_pk'),
        {'schema': 'COCCDM'}
    )

    encompassid: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    applicationid: Mapped[str] = mapped_column(VARCHAR(100), primary_key=True)
    incomeid: Mapped[str] = mapped_column(VARCHAR(50), primary_key=True)
    amount: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    owner: Mapped[Optional[str]] = mapped_column(VARCHAR(25))
    incometype: Mapped[Optional[str]] = mapped_column(VARCHAR(25))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('SYSDATE'))


class Encloan(Base):
    __tablename__ = 'encloan'
    __table_args__ = (
        PrimaryKeyConstraint('encompassid', name='encloan_pk'),
        {'schema': 'COCCDM'}
    )

    encompassid: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    baseloanamount_2: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    requestedinterestratepercent_3: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    loanamortizationtermmonths_4: Mapped[Optional[int]] = mapped_column(Integer)
    prinandintmthlypayamt_5: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    regulationz_pmiindicator_8: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    property_streetaddress_11: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    property_city_12: Mapped[Optional[str]] = mapped_column(VARCHAR(22))
    property_county_13: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    state_14: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    postalcode_15: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    financednumberofunits_16: Mapped[Optional[int]] = mapped_column(Integer)
    legaldescriptiontext1_17: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    structurebuiltyear_18: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    loanpurposetype_19: Mapped[Optional[str]] = mapped_column(VARCHAR(25))
    gsetitlemannerhelddesc_33: Mapped[Optional[str]] = mapped_column(VARCHAR(24))
    gserefinancepurposetype_299: Mapped[Optional[str]] = mapped_column(VARCHAR(32))
    propertyexistinglienamount_10: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    propertyacquiredyear_20: Mapped[Optional[str]] = mapped_column(VARCHAR(6))
    propertyoriginalcostamount_21: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    landestimatedvalueamount_22: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    constructionimprovecostsamt_23: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    otherloanpurposedescription_9: Mapped[Optional[str]] = mapped_column(VARCHAR(8))
    onetimeclose_urla_x192: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    twotimeclose_urla_x193: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    loanpurposetypeurla_urla_x71: Mapped[Optional[str]] = mapped_column(VARCHAR(24))
    loanpurptypotherdesc_urlax72: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    addresslinetext_urlax73: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    addrsunitdesignatortyp_urlax74: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    addressunitidentifier_urlax75: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    fhasecresidenceind_urlax76: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    propertymixedusageind_urlax77: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    sellsiderequestedby_2030: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    prepaypenalty_2216: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    sellsideratesheetid_2219: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    sellsidelockdate_2220: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    sellsidenumberofdays_2221: Mapped[Optional[int]] = mapped_column(Integer)
    sellsidelockexpires_2222: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    sellsiderate_2223: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    sellsideratetotaladj_2230: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    sellsidenetsellrate_2231: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    sellsidepricerate_2232: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    sellsidepricetotaladj_2273: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    sellsidenetsellprice_2274: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    sellsidesrppaidout_2276: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    investorname_2278: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    impoundwavied_2293: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    impoundtype_2294: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    gainlosstotalbuyprice_2295: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    date_2370: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    amountdueto_2627: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    amountdue_2631: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    sellsidemargintotaladj_2817: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    sellsidemargnetsellrt_2818: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    comments_2840: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    datesold_3337: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    servicingreleaseind_3338: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    datewarehoused_3341: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    balloonlnmtritytrmmthscnt_325: Mapped[Optional[int]] = mapped_column(Integer)
    loanproddata_lienprtytyp_420: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    prepaymentpenaltyindicator_675: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    scheduledfirstpaymentdate_682: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    indexcurrentvaluepercent_688: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    indexmarginpercent_689: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    balloonindicator_1659: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    qualifyingratepercent_1014: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borrowerestclosingdate_4114: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    fnmproductplanidentifier_995: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    loandocumentationtyp_mornetx67: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    nmlsloantype_nmlsx1: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    nmlsreversemortgagetyp_nmlsx10: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    initialapplicamt_nmlsx11: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    netinitialandfinal_nmlsx12: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    inquiryorprequalind_nmlsx13: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    oralrstextofcrditind_nmlsx14: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    excldelnfrmnmlsrptind_nmlsx15: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    nmlspropertytype_nmlsx16: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    nmlslienstatus_nmlsx17: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    nmlsfirstmortgagetype_nmlsx2: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    nmlsdocumentationtype_nmlsx3: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    nmlsoptionarmindicator_nmlsx4: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    nmlspigbckorfndhelocind_nmlsx5: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    nmlsrefipurptype_nmls_x6: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    nmlsprodsoldtotype_nmls_x7: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    pmiindicator_8: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    aprpercent_799: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    mimonthlypaymentlevel1_1766: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    interestonlyindicator_2982: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    gfeapplicationdate_3142: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    totalbrokerfees_3310: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    totallenderfees_3311: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    interestreserveamount_1265: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    years_1266: Mapped[Optional[int]] = mapped_column(Integer)
    ratepercent_1267: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    finalpaymentdate_1961: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    firstamortpaydate_1963: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    acquisition_1964: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    initialdisclosureduedate_3143: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    earliestfeecollectiondate_3145: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    earliestclosingdate_3147: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    inittildisclosureprovdt_3152: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    inittildisrcvddt_3153: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    tilredisclosprovdt_3154: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    tilredisclosrcvddt_3155: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    borrowintendtocontdt_3197: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    initgfeaffltdbusiprovdt_3544: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    initgfecharmbookletprovdt_3545: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    initgfehudspclbkletprovdt_3546: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    initgfehelocbrochprovdt_3547: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    initgfeapprslprovdt_3624: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    initsubapprslprovdt_3857: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    initialavmprovideddate_3858: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    homecounselingprovdt_3859: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    closingdisclsentdt_3977: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    closingdisclrcvddt_3978: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    revisedclosingdiscsntdt_3979: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    revisedclosingdisclrcvddt_3980: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    postconsumdisclsntdt_3981: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    postconsumdisclsrcvddt_3982: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    esignconsentdate_3983: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ssplsentdate_4014: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    safeharborsentdate_4015: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    highcostdisclosure_4022: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    occupancycertdate_4080: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    construcrefiind_constr_refi: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    constructionloanmethod_sys_x6: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    prdincinlntrmflg_const_x1: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cntrctiss_const_x10: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    commitmentletterdate_constx11: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    commitexpirdate_constx12: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    rtnlendcpycommtdays_constx14: Mapped[Optional[int]] = mapped_column(Integer)
    takeoutcommitind_constx15: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    takeoutcommit_constx16: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    titleinsind_constx17: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    titleinsurancedate_constx18: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    surveyindicator_constx19: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    securedbysepprop_constx2: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    surveydate_constx20: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    permitsindicator_constx21: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    permitsdateconstx22: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    utilityltrsindconstx23: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    utilitylettersdateconstx24: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    plansandspec_constx25: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    plansandspecdate_constx26: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    constcontind_constx27: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    constcontractrecddt_constx28: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    budgetindicator_constx29: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    constcompletiondate_constx3: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    budgetdate_constx30: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    contractorsagree_constx31: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    contractorsagreedate_constx32: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    architectscert_constx33: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    architectscertdate_constx34: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    enviassessment_constx35: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    enviassessmentdate_constx36: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    soilreportindicator_constx37: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    soilreportdate_constx38: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    watertestindicator_constx39: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    watertestdate_constx40: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    percolationtest_constx41: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    percolationtestdate_constx42: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    paymentandperbonds_constx43: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    paymentandperbonds_constx44: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    lienagentnc_constx45: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    lienagentnc_constx46: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    floodhazarddet_constx47: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    floodhazarddet_constx48: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    listofconstagree_constx49: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    maxltvpercent_constx5: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    listofconstagree_constx50: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    otherindicator_constx51: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    otherdate_constx52: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    otherdescription_constx53: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    futureadvanceperiod_constx54: Mapped[Optional[int]] = mapped_column(Integer)
    mindaysbetweendisb_constx55: Mapped[Optional[int]] = mapped_column(Integer)
    partialprepayelect_constx57: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ascomppurchaseprice_constx58: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    ascompappraisedvalue_constx59: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    holdbackpercent_constx7: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    holdbackamount_constx8: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    projdelaysurchrgpct_constx9: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    investorloannumber_352: Mapped[Optional[str]] = mapped_column(VARCHAR(18))
    ausrecommendation_1544: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    required_1546: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    verified_1547: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    numberofmonthsreserves_1548: Mapped[Optional[int]] = mapped_column(Integer)
    interestedpartycontrib_1549: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    unpaidbalance_1732: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    submitteddate_2298: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    resubmitteddate_2299: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    creditapprovaldate_2300: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    approveddate_2301: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    approvalexpireddate_2302: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    suspendeddate_2303: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    signoffdate_2304: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    cleartoclosedate_2305: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    miordereddate_2308: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    mireceiveddate_2309: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    maxrate_2310: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    suspendedreasons_2311: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    aussource_2312: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ausrundate_2313: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ausreviewdate_2314: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    signoffby_2315: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ausnumber_2316: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    exceptionsignoffdate_2317: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    exceptionsignoffby_2318: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    strengths_2319: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    concerns_2320: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    credit_2321: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    appraisal_2322: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    exceptions_2323: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    originalappraiser_2351: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    appraisalordereddate_2352: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    appraisalcompleteddate_2353: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    appraisalexpireddate_2354: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    originalappraisersvalue_2355: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    appraisaltype_2356: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    reviewappraiser_2357: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    reviewrequesteddate_2359: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    reviewcompleteddate_2360: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    reviewvalue_2361: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    conditions_2362: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    senttodate_2981: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    benefitrequiredindicator_2983: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    approvedby_2984: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    suspendedby_2985: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    deniedby_2986: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    denieddate_2987: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    differentapprovedby_2988: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    differentapproveddate_2989: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    diffappexpdt_2990: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    modifiedloanamount_2991: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    modifiedloanrate_2992: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    modifiedloanterm_2993: Mapped[Optional[int]] = mapped_column(Integer)
    modifiedmonthlypayment_2994: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    modifiedltv_2995: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    isagencywithagreement_3878: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    isagencywaiver_3879: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    isagencymanually_3880: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    counterofferdate_4457: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    fhavaloan_closingdate_748: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    fhavaloan_propmatyr_1347: Mapped[Optional[int]] = mapped_column(Integer)
    fhavaloan_giftfundsamount_220: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    loannumber_364: Mapped[Optional[str]] = mapped_column(VARCHAR(22))
    loansub_numberofdays_432: Mapped[Optional[int]] = mapped_column(Integer)
    loanamortizationtype_608: Mapped[Optional[str]] = mapped_column(VARCHAR(6))
    closingcost_escrowconm_610: Mapped[Optional[str]] = mapped_column(VARCHAR(22))
    originationdate_745: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    adverseactiondate_749: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    loansubmission_lockdate_761: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    loansub_lockexpires_762: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    loanschedclosingdate_763: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    gsepropertytype_1041: Mapped[Optional[str]] = mapped_column(VARCHAR(28))
    borrpaiddiscpointsamt_1093: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borrowerreqloanamt_1109: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    mortgagetype_1172: Mapped[Optional[str]] = mapped_column(VARCHAR(12))
    interestonlymonths_1177: Mapped[Optional[int]] = mapped_column(Integer)
    loanprogramname_1401: Mapped[Optional[str]] = mapped_column(VARCHAR(248))
    downpaymentpercent_1771: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    closingcostprogram_1785: Mapped[Optional[str]] = mapped_column(VARCHAR(14))
    disbursementdate_2553: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    currentratesetdate_3253: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    signaturedatefor1003_3261: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    closingdocument_plancode_1881: Mapped[Optional[str]] = mapped_column(VARCHAR(14))
    repurchasedate_3312: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    repurchasecostamount_3313: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    conformingjumbo_3331: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    lenderchannel_3332: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    occupancytype_3335: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    pmiindicator_3336: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    isemployeeloan_4181: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    usepitiforratio_1853: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    documentsigningdate_1887: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    downpayment_sourcedesc_191: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    perdiemcalcmethtype_1962: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    loansource_2024: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    loancreateddateutc_2025: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    loanislocked_2400: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    leadsource_2976: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ratelockdisclosuredate_3259: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    undiscountedrate_3293: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    enforcecountyloanlimit_3894: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    secondaryregistration_3941: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    isreqintrescompint_4086: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    iscreditorprohibitsborr_4087: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    estimatedconstint_4088: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    paymentfreqtype_423: Mapped[Optional[str]] = mapped_column(VARCHAR(8))
    buydownindicator_425: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    loansubmission_ratelock_431: Mapped[Optional[str]] = mapped_column(VARCHAR(12))
    specfloodhazardarea_541: Mapped[Optional[str]] = mapped_column(VARCHAR(8))
    prophousingexptotal_912: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    combinedltv_976: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    otheramorttypedescr_994: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    reqdoctype_casasrnx144: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    reserves_casasrnx78: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    cddateissued_cd1x1: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    stmtcreddenial_denial_x69: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    closingdocument_resc_l724: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    docpreparationdate_l770: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    organizationcode_orgid: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    atrqmcommon_atrloantype_qmx23: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    iseligibleforsafeharbor_qmx25: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ratesetindex_s32disc: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    mortgageaccount_servicex1: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    payduedateprint_servicex10: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    nextpaystmtdue_servicex13: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    servicingstatus_servicex8: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    laststmtprinted_servicex9: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    trustaccount_bal_tabalance: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    trustaccount_total1_tatotal1: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    trustaccount_total2_tatotal2: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    tpo_underwritingdel_tpox88: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    tql_currinvestpubstat_tqlx1: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    uldd_constmethodtype_ulddx172: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    urlaloanidentifier_urlax120: Mapped[Optional[str]] = mapped_column(VARCHAR(45))
    affordableloan_urlax210: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    loandonotapply_urlax237: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    printuliandloanno_urlax238: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    negativeamortization_urlax239: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    prepaypenterm_urlax240: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    temporiniintratebuy_urlax241: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    loanfeaturesother_urlax242: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    expectborrcount_urlax261: Mapped[Optional[int]] = mapped_column(Integer)
    printlenderpages_urlax231: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    coremilestone: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    currentteammember: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    propertyappraisedvalueamt_356: Mapped[Optional[int]] = mapped_column(Integer)
    aprdisclosuredate_363: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    pointspaid_1191: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    refundoroverpaidinterest_1192: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borrowerdescription1_1193: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borrowerdescription2_1194: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borrowerdescription3_1195: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    taxid_1196: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    docsetfile_2863: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    registeredby_2822: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    registrationdate_2823: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    expirationdate_2824: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    registrationinvestorname_2825: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    registrationreference_2826: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    maventreviewresult_x1: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    maventofacresult_x10: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    maventtilatolrslt_comp_x14: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    maventhpmlresult_x16: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    maventnmlsresult_x17: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    maventhmdaresultx8: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    loanpurpose_384: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    msanumber_699: Mapped[Optional[str]] = mapped_column(VARCHAR(14))
    censustrack_700: Mapped[Optional[str]] = mapped_column(VARCHAR(14))
    actiontaken_1393: Mapped[Optional[str]] = mapped_column(VARCHAR(52))
    statecode_1395: Mapped[Optional[str]] = mapped_column(VARCHAR(14))
    countycode_1396: Mapped[Optional[str]] = mapped_column(VARCHAR(14))
    typeofpurchaser_1397: Mapped[Optional[str]] = mapped_column(VARCHAR(24))
    hmdaprofileid_hmdax100: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    legalentityidentrpt_hmdax106: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    hmdaloanpurpose_hmdax107: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    propvalnotreliedupon_hmdax108: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    hmdainterestonly_hmdax109: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    propertytype_hmdax11: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    incomeexcfrom_hmdax110: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    hmdacountycode_hmdax111: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    hmdacensustrack_hmdax112: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    partiallyexemptloan_hmdax113: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    balloon_hmdax114: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    loanbalancerise_hmdax115: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    preapprovals_hmdax12: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    hmda2interestonly_hmdax120: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    hoepastatus_hmdax13: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    lienstatus_hmdax14: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    ratespread_hmdax15: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    denialreason1_hmdax21: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    denialreason2_hmdax22: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    denialreason3_hmdax23: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    excludeloanfromreport_hmdax24: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    qmstatus_hmdax26: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    reportingyear_hmdax27: Mapped[Optional[int]] = mapped_column(Integer)
    universalloanid_hmdax28: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    applicationdate_hmdax29: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    loantype_hmdax30: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    loanamount_hmdax31: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    income_hmdax32: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    denialreason4_hmdax33: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otherdenialreason_hmdax34: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    discountpoints_hmdax35: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    debttoincomeratio_hmdax36: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    cltv_hmdax37: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    othernonamortization_hmdax38: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    manufacsecurproptype_hmdax39: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    manufachomlanpropint_hmdax40: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    multifamilynounits_hmdax41: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    subofapplication_hmdax42: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    initialpaytoyourinst_hmdax43: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    aus1_hmdax44: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    aus2_hmdax45: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    aus3_hmdax46: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    aus4_hmdax47: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    aus5_hmdax48: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otheraus_hmdax49: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ausrecommendation1_hmdax50: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ausrecommendation2_hmdax51: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ausrecommendation3_hmdax52: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ausrecommendation4_hmdax53: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ausrecommendation5_hmdax54: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    otherausrec_hmdax55: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    reversemortgage_hmdax56: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    openendlineofcredit_hmdax57: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    busiorcommpurp_hmdax58: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    financialinstname_hmdax59: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    contactname_hmdax60: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    contactphonenumber_hmdax61: Mapped[Optional[str]] = mapped_column(VARCHAR(17))
    contactemailaddress_hmdax62: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    contactofficestadd_hmdax63: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    contactofficecity_hmdax64: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    contactofficestate_hmdax65: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    contactofficezipcode_hmdax66: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    contactfaxnumber_hmdax67: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    federalagency_hmdax68: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    fedtaxpayeridnbr_hmdax69: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    legalentityidentifier_hmdax70: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    respondentid_hmdax71: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    parentname_hmdax72: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    parentaddress_hmdax73: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    parentcity_hmdax74: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    parentstate_hmdax75: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    parentzip_hmdax76: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    totalloancosts_hmdax77: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    totalpointsandfees_hmdax78: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    originationcharges_hmdax79: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    lendercredits_hmdax80: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    interestrate_hmdax81: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    prepaypenper_hmdax82: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    loanterm_hmdax83: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    introrateperiod_hmdax84: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    propertyvalue_hmdax85: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    nmlsloanoriginatorid_hmdax86: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    hmdapropertyzipcode_hmdax87: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    hmdapropertyaddress_hmdax88: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    hmdapropertycity_hmdax89: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    hmdapropertystate_hmdax90: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    repurchasedreportyr_hmdax92: Mapped[Optional[int]] = mapped_column(Integer)
    repurchasedloanamount_hmdax93: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    repurchasedtypeofpurc_hmdax94: Mapped[Optional[str]] = mapped_column(VARCHAR(24))
    repurchactiontaken_hmdax95: Mapped[Optional[str]] = mapped_column(VARCHAR(52))
    repurchasedactiondate_hmdax96: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    hmdadtiindicator_hmdax97: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    hmdacltvindicator_hmdax98: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    hmdaincomeindicator_hmdax99: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    purchasepriceamount_136: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    estprepaiditemsamount_138: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    proposedfirstmortamount_228: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    proposedhazardinsamount_230: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    proposedmortinsamount_232: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    lendercaseidentifier_305: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    fanniemae_ltv_353: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    ltvpropertyvalue_358: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    secondsubordinateamount_428: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    firsttimehomebuyers_934: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    agencycaseidentifier_1040: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    mersnumber_1051: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    interviewername_1612: Mapped[Optional[str]] = mapped_column(VARCHAR(16))
    propertyestvalueamt_1821: Mapped[Optional[int]] = mapped_column(Integer)
    referralsource_1822: Mapped[Optional[str]] = mapped_column(VARCHAR(24))
    print2003application_1825: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    totaldeductionsamount_1989: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    totalwiretransferamount_1990: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    funding_fundssentdate_1997: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    overwireamount_2005: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    shipping_actualshipdate_2014: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    channel_2626: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    section32_sec35avgprmrt_3134: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    nmlsloanoriginatorid_3238: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    use2018diindicator_4142: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrowerpaircount_4460: Mapped[Optional[int]] = mapped_column(Integer)
    subpropgrossrentincamt_1005: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    subjectpropoccuppct_1487: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    printulionurla_urla_x119: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    borrcommpropstresi_urla_x129: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    conofcontfordeed_urla_x131: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    renovationloan_urla_x132: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    constructionloan_urla_x133: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    consttopermclosing_urla_x134: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    propexstclnenerlien_urla_x135: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    titlewillbefullname_urla_x136: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    titleholderfullname_urla_x137: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    relvestingtype_urla_x138: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    relvesttypeotherdes_urla_x139: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    trustclassitype_urla_x140: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    nativeamerlandstype_urla_x141: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    natamelndstypotrdes_urla_x142: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    productdescription_urla_x143: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    supplepropinsamt_urla_x144: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    nonsubprodebpdoffam_urla_x145: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    borrestcloscostsamt_urla_x146: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    totalsubordfinamt_urla_x147: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    urlatotalmortlnsamt_urla_x148: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    totalothercrditsamt_urla_x149: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    totalofgiftsgrants_urla_x150: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    totalotherassetloan_urla_x151: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    totalcreditsamt_urla_x152: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    housingcounselag_urla_x156: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    ownershipcomp_urla_x157: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    borrowerfullname_urla_x158: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    counselagfullname_urla_x162: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    counselingcompdt_urla_x163: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    counselborrfullna_urla_x164: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    reficashoutdetertyp_urla_x165: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    gmentrefitype_urla_x166: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    originatorfirstname_urla_x170: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    origmiddlename_urla_x171: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    originatorlastname_urla_x172: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    origrsuffixname_urla_x173: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    origaddlinetext_urla_x188: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    origaddunitdestyp_urla_x189: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    origaddunitiden_urla_x190: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    borrowercount_urla_x194: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    condominiumind_urla_x205: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    cooperativeindicator_urla_206: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    pudindicator_urla_207: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    notinproject_urla_208: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    paydeffirstfiveyears_urla_209: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    rentalincomesec_urla_x80: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    estnetmthlyrentamt_urla_x81: Mapped[Optional[float]] = mapped_column(NUMBER(asdecimal=False))
    creditscore_vasumm_x23: Mapped[Optional[int]] = mapped_column(Integer)
    titleholdername1_31: Mapped[Optional[str]] = mapped_column(VARCHAR(22))
    edisclosedtrk_disclosurecount: Mapped[Optional[int]] = mapped_column(Integer)
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('SYSDATE'))


class Encresidences(Base):
    __tablename__ = 'encresidences'
    __table_args__ = (
        PrimaryKeyConstraint('encompassid', 'applicationid', 'residenceid', name='encresidences_pk'),
        {'schema': 'COCCDM'}
    )

    encompassid: Mapped[str] = mapped_column(VARCHAR(36), primary_key=True)
    applicationid: Mapped[str] = mapped_column(VARCHAR(100), primary_key=True)
    residenceid: Mapped[str] = mapped_column(VARCHAR(50), primary_key=True)
    addressstreetline1: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    addresscity: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    addressstate: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    addresspostalcode: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    addressunitdesignatortype: Mapped[Optional[str]] = mapped_column(VARCHAR(52))
    addressunitdesignatortype_1: Mapped[Optional[str]] = mapped_column(VARCHAR(52))
    addressunitidentifier: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    addressunitidentifier_1: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    countrycode: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    countrycode_1: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    residencedoesnotapplyind: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    rent: Mapped[Optional[int]] = mapped_column(Integer)
    rent_1: Mapped[Optional[int]] = mapped_column(Integer)
    urla2020streetaddress: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    applicanttype: Mapped[Optional[str]] = mapped_column(VARCHAR(15))
    mailingaddressindicator: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    residencytype: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('SYSDATE'))


t_fin_budgetitem = Table(
    'fin_budgetitem', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('userid', VARCHAR(32)),
    Column('dataspace', VARCHAR(10)),
    Column('iskeyexpense', VARCHAR(5)),
    Column('categoryname', VARCHAR(100)),
    Column('budgetamount', NUMBER(19, 4, True), nullable=False),
    Column('insertdateutc', DateTime, nullable=False),
    schema='COCCDM'
)


t_fin_categorizationstats = Table(
    'fin_categorizationstats', Base.metadata,
    Column('statisiticsid', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('dateutc', DateTime, nullable=False),
    Column('userid', VARCHAR(32)),
    Column('totaltransactioncount', NUMBER(10, 0, False), nullable=False),
    Column('transactionsautocategorized', NUMBER(10, 0, False), nullable=False),
    Column('txnscategorizedusingmcc', NUMBER(10, 0, False), nullable=False),
    Column('txnscategorizedusingtyporregex', NUMBER(10, 0, False), nullable=False),
    Column('txnscategorizedusingprefix', NUMBER(10, 0, False), nullable=False),
    Column('txnscategorizedasdefault', NUMBER(10, 0, False), nullable=False),
    Column('txswithmcccodeunmapped', NUMBER(10, 0, False), nullable=False),
    Column('transactionswithoutmcccode', NUMBER(10, 0, False), nullable=False),
    Column('timetocategorizems', NUMBER(10, 0, False)),
    Column('txncountusercategorizer', NUMBER(10, 0, False)),
    Column('txnscategorizedwithuserovrd', NUMBER(10, 0, False)),
    schema='COCCDM'
)


t_fin_categorizationstats_temp = Table(
    'fin_categorizationstats_temp', Base.metadata,
    Column('statisiticsid', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('dateutc', DateTime, nullable=False),
    Column('userid', VARCHAR(32)),
    Column('totaltransactioncount', NUMBER(10, 0, False), nullable=False),
    Column('transactionsautocategorized', NUMBER(10, 0, False), nullable=False),
    Column('txnscategorizedusingmcc', NUMBER(10, 0, False), nullable=False),
    Column('txnscategorizedusingtyporregex', NUMBER(10, 0, False), nullable=False),
    Column('txnscategorizedusingprefix', NUMBER(10, 0, False), nullable=False),
    Column('txnscategorizedasdefault', NUMBER(10, 0, False), nullable=False),
    Column('txswithmcccodeunmapped', NUMBER(10, 0, False), nullable=False),
    Column('transactionswithoutmcccode', NUMBER(10, 0, False), nullable=False),
    Column('timetocategorizems', NUMBER(10, 0, False)),
    Column('txncountusercategorizer', NUMBER(10, 0, False)),
    Column('txnscategorizedwithuserovrd', NUMBER(10, 0, False)),
    schema='COCCDM'
)


t_fin_preferences_includedaccts = Table(
    'fin_preferences_includedaccts', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('accountid', VARCHAR(100)),
    Column('userid', VARCHAR(32)),
    Column('insertdateutc', DateTime, nullable=False),
    schema='COCCDM'
)


t_fin_savingsgoal = Table(
    'fin_savingsgoal', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('userid', VARCHAR(32)),
    Column('linkedaccountid', VARCHAR(100)),
    Column('nickname', VARCHAR(100)),
    Column('goal', NUMBER(19, 4, True), nullable=False),
    Column('startdate', DateTime),
    Column('targetdate', DateTime),
    Column('startingpointbalance', NUMBER(19, 4, True)),
    Column('displayinsummary', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    schema='COCCDM'
)


class Goal(Base):
    __tablename__ = 'goal'
    __table_args__ = (
        PrimaryKeyConstraint('goalnbr', name='pk_goal'),
        {'schema': 'COCCDM'}
    )

    goalnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '))
    goaldesc: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    targetcount: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    targetamount: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(23, 3, True))
    startdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    enddate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    goaltypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    incentiveplnnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))


class Goalproduct(Base):
    __tablename__ = 'goalproduct'
    __table_args__ = (
        PrimaryKeyConstraint('goalproductnbr', 'goalnbr', name='pk_goalproduct'),
        {'schema': 'COCCDM'}
    )

    goalproductnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    goalnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '))
    mjaccttypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    miaccttypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    agreetypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    userfieldcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))


class Goalteam(Base):
    __tablename__ = 'goalteam'
    __table_args__ = (
        PrimaryKeyConstraint('goalnbr', 'teamnbr', name='pk_goalteam'),
        {'schema': 'COCCDM'}
    )

    goalnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    teamnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '))
    targetcount: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    targetamount: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(23, 3, True))


class Goalteampers(Base):
    __tablename__ = 'goalteampers'
    __table_args__ = (
        PrimaryKeyConstraint('goalnbr', 'teamnbr', 'persnbr', name='pk_goalteampers'),
        {'schema': 'COCCDM'}
    )

    goalnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    teamnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    persnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '))
    targetcount: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    targetamount: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(23, 3, True))


class Househld(Base):
    __tablename__ = 'househld'
    __table_args__ = (
        PrimaryKeyConstraint('householdnbr', name='pk_househld'),
        {'schema': 'COCCDM'}
    )

    householdnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    datecreated: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '))
    householdtitle: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    headofhousenbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    headofhousetyp: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    branchorgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    singleserviceyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    statuscd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    addrnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))


class Househldacct(Base):
    __tablename__ = 'househldacct'
    __table_args__ = (
        PrimaryKeyConstraint('householdnbr', 'acctnbr', 'persnbr', 'orgnbr', name='pk_househldacct'),
        {'schema': 'COCCDM'}
    )

    householdnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    persnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    orgnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    datecreated: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '))
    statuscd: Mapped[Optional[str]] = mapped_column(VARCHAR(3))
    primaryacct: Mapped[Optional[str]] = mapped_column(CHAR(1))


t_ib_entitlement = Table(
    'ib_entitlement', Base.metadata,
    Column('userid', NUMBER(19, 0, False), nullable=False, comment='iBanking User ID'),
    Column('businessuserid', NUMBER(19, 0, False), comment='Business User ID if the user is a business user'),
    Column('entitlementname', VARCHAR(512), nullable=False, comment='Friendly name of the iBanking entitlement'),
    Column('entitlementvalue', VARCHAR(128), nullable=False, comment='Effective value of the iBanking entitlement'),
    Column('definitionid', VARCHAR(128), nullable=False, comment='Unique GUID of the iBanking entitlement'),
    Column('parentdefinitionid', VARCHAR(128), comment='Unique GUID of the parent entitlement of the iBanking entitlement'),
    Column('haschildrenwithkeys', NUMBER(1, 0, False), nullable=False, server_default=text('0 '), comment='If the entitlement has children with keys or not.  1 if entitlement has children with keys and 0 if entitlement has no children with keys.'),
    Column('propertyname', VARCHAR(128), nullable=False, comment='Name of the entitlement value property'),
    Column('effectivedate', DateTime, nullable=False, server_default=text('sysdate '), comment='Date entitlement was effective'),
    Column('endeffectivedate', DateTime, comment='Date entitlement value was not effective'),
    Column('entitlementtree', VARCHAR(512), nullable=False, comment='Tree of entitlement name with names of parent entitlements'),
    Column('depth', NUMBER(asdecimal=False), nullable=False, comment='Depth of entitlement in the entitlement hierarchy'),
    Column('isactive', NUMBER(1, 0, False), nullable=False, server_default=text('0 ')),
    CheckConstraint('HasChildrenWithKeys in (0, 1)', name='haschildrenwithkeysis0or1'),
    CheckConstraint('ISACTIVE in (0, 1)', name='isactiveis0or1'),
    Index('ib_entitlement_idx1', 'userid', 'isactive', 'definitionid', 'entitlementname', 'entitlementvalue'),
    schema='COCCDM'
)


t_ibankingdisclosures = Table(
    'ibankingdisclosures', Base.metadata,
    Column('dataspace', VARCHAR(50)),
    Column('userid', VARCHAR(50)),
    Column('disclosureid', NUMBER(19, 0, False), nullable=False),
    Column('name', VARCHAR(100)),
    Column('disclosureversionid', NUMBER(19, 0, False), nullable=False),
    Column('version', NUMBER(19, 0, False), nullable=False),
    Column('isaccepted', VARCHAR(5)),
    Column('isresetbyadmin', VARCHAR(5)),
    Column('actiondate', DateTime, nullable=False),
    schema='COCCDM'
)


t_ibankingusers = Table(
    'ibankingusers', Base.metadata,
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('useridtxt', VARCHAR(40)),
    Column('institutionuserid', VARCHAR(32)),
    Column('loginname', VARCHAR(101)),
    Column('status', VARCHAR(8)),
    Column('isadmin', VARCHAR(1)),
    Column('persnbr', NUMBER(asdecimal=False)),
    Column('orgnbr', NUMBER(asdecimal=False)),
    Column('agreenbr', NUMBER(asdecimal=False)),
    Column('name', VARCHAR(60)),
    Column('sortname', VARCHAR(60)),
    Column('taxid', VARCHAR(60)),
    Column('datebirth', DateTime),
    Column('extcardnbr', VARCHAR(32)),
    Column('home', VARCHAR(22)),
    Column('work', VARCHAR(22)),
    Column('cell', VARCHAR(22)),
    schema='COCCDM'
)


t_ids_featureset = Table(
    'ids_featureset', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('name', VARCHAR(50)),
    schema='COCCDM'
)


t_ids_featuresetfeature = Table(
    'ids_featuresetfeature', Base.metadata,
    Column('featuresetid', NUMBER(19, 0, False), nullable=False),
    Column('definitionid', VARCHAR(40)),
    Column('key', VARCHAR(100)),
    Column('propertyname', VARCHAR(50)),
    Column('value', VARCHAR(50)),
    schema='COCCDM'
)


t_ids_rsauser = Table(
    'ids_rsauser', Base.metadata,
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('rsauserid', VARCHAR(50)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_ids_user = Table(
    'ids_user', Base.metadata,
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('title', VARCHAR(32)),
    Column('firstname', VARCHAR(64)),
    Column('middlename', VARCHAR(64)),
    Column('lastname', VARCHAR(256)),
    Column('suffix', VARCHAR(32)),
    Column('birthdate', DateTime),
    Column('primaryaddressid', NUMBER(19, 0, False)),
    Column('primaryemailid', NUMBER(19, 0, False)),
    Column('primaryphoneid', NUMBER(19, 0, False)),
    Column('recorddeleted', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('updatedateutc', DateTime, nullable=False),
    Column('updatingappname', VARCHAR(50)),
    Column('updatingprocname', VARCHAR(50)),
    Column('updatinguserid', VARCHAR(50)),
    Column('status', NUMBER(3, 0, False)),
    Column('timezone', VARCHAR(50)),
    Column('preferredculture', VARCHAR(20)),
    Column('prefculturechangedatetimeutc', DateTime),
    Column('dataspace', VARCHAR(10)),
    schema='COCCDM'
)


t_ids_useraddress = Table(
    'ids_useraddress', Base.metadata,
    Column('useraddressid', NUMBER(19, 0, False), nullable=False),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('addresstypeid', NUMBER(10, 0, False), nullable=False),
    Column('streetaddress', VARCHAR(512)),
    Column('city', VARCHAR(32)),
    Column('state', VARCHAR(8)),
    Column('postalcode', VARCHAR(16)),
    Column('countrycode', VARCHAR(8)),
    Column('recorddeleted', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('updatedateutc', DateTime, nullable=False),
    Column('updatingappname', VARCHAR(50)),
    Column('updatingprocname', VARCHAR(50)),
    Column('updatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_ids_useremail = Table(
    'ids_useremail', Base.metadata,
    Column('useremailid', NUMBER(19, 0, False), nullable=False),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('emailaddress', VARCHAR(256)),
    Column('recorddeleted', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('updatedateutc', DateTime, nullable=False),
    Column('updatingappname', VARCHAR(50)),
    Column('updatingprocname', VARCHAR(50)),
    Column('updatinguserid', VARCHAR(50)),
    Column('emailtypeid', NUMBER(10, 0, False)),
    schema='COCCDM'
)


t_ids_useridentification = Table(
    'ids_useridentification', Base.metadata,
    Column('useridentificationid', NUMBER(19, 0, False), nullable=False),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('identificationtypeid', NUMBER(10, 0, False), nullable=False),
    Column('identificationvalue', VARCHAR(64)),
    Column('issuedate', DateTime),
    Column('expirationdate', DateTime),
    Column('issuedby', VARCHAR(32)),
    Column('recorddeleted', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('updatedateutc', DateTime, nullable=False),
    Column('updatingappname', VARCHAR(50)),
    Column('updatingprocname', VARCHAR(50)),
    Column('updatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_ids_userphone = Table(
    'ids_userphone', Base.metadata,
    Column('userphoneid', NUMBER(19, 0, False), nullable=False),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('phonetypeid', NUMBER(10, 0, False), nullable=False),
    Column('phonenumber', VARCHAR(24)),
    Column('extension', VARCHAR(16)),
    Column('recorddeleted', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('updatedateutc', DateTime, nullable=False),
    Column('updatingappname', VARCHAR(50)),
    Column('updatingprocname', VARCHAR(50)),
    Column('updatinguserid', VARCHAR(50)),
    schema='COCCDM'
)


t_ids_usersecurity = Table(
    'ids_usersecurity', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('loginname', VARCHAR(101)),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('passwordhash', VARCHAR(512)),
    Column('passwordexpirationdateutc', DateTime),
    Column('lastlogindateutc', DateTime),
    Column('lastloginfailuredateutc', DateTime),
    Column('consecutiveloginfailures', NUMBER(10, 0, False), nullable=False),
    Column('changepasswordrequired', VARCHAR(5)),
    Column('recorddeleted', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    Column('insertingappname', VARCHAR(50)),
    Column('insertingprocname', VARCHAR(50)),
    Column('insertinguserid', VARCHAR(50)),
    Column('updatedateutc', DateTime, nullable=False),
    Column('updatingappname', VARCHAR(50)),
    Column('updatingprocname', VARCHAR(50)),
    Column('updatinguserid', VARCHAR(50)),
    Column('changeloginnamecount', NUMBER(10, 0, False), nullable=False),
    Column('lastpasswordchangedatetimeutc', DateTime),
    schema='COCCDM'
)


t_ids_v_useraddress = Table(
    'ids_v_useraddress', Base.metadata,
    Column('useraddressid', NUMBER(19, 0, False), nullable=False),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('addresstypeid', NUMBER(10, 0, False), nullable=False),
    Column('description', VARCHAR(32)),
    Column('streetaddress', VARCHAR(512)),
    Column('city', VARCHAR(32)),
    Column('state', VARCHAR(8)),
    Column('postalcode', VARCHAR(16)),
    Column('countrycode', VARCHAR(8)),
    Column('recorddeleted', VARCHAR(5)),
    Column('updatedateutc', DateTime, nullable=False),
    schema='COCCDM'
)


t_ids_v_useridentification = Table(
    'ids_v_useridentification', Base.metadata,
    Column('useridentificationid', NUMBER(19, 0, False), nullable=False),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('description', VARCHAR(32)),
    Column('identificationvalue', VARCHAR(64)),
    Column('issuedate', DateTime),
    Column('expirationdate', DateTime),
    Column('issuedby', VARCHAR(32)),
    Column('recorddeleted', VARCHAR(5)),
    Column('updatedateutc', DateTime, nullable=False),
    schema='COCCDM'
)


t_ids_v_userphone = Table(
    'ids_v_userphone', Base.metadata,
    Column('userphoneid', NUMBER(19, 0, False), nullable=False),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('phonetypeid', NUMBER(10, 0, False), nullable=False),
    Column('description', VARCHAR(32)),
    Column('phonenumber', VARCHAR(24)),
    Column('extension', VARCHAR(16)),
    Column('recorddeleted', VARCHAR(5)),
    Column('updatedateutc', DateTime, nullable=False),
    schema='COCCDM'
)


t_insight_ofx_directconnectuser = Table(
    'insight_ofx_directconnectuser', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('allowpersonal', VARCHAR(5)),
    Column('allowbusiness', VARCHAR(5)),
    Column('lastactivityutc', DateTime),
    Column('isdeleted', VARCHAR(5)),
    Column('insertinguserid', NUMBER(19, 0, False), nullable=False),
    Column('insertingdateutc', DateTime, nullable=False),
    Column('updatinguserid', NUMBER(19, 0, False), nullable=False),
    Column('updatingdateutc', DateTime, nullable=False),
    schema='COCCDM'
)


t_insight_ofx_messagethreads = Table(
    'insight_ofx_messagethreads', Base.metadata,
    Column('threadid', NUMBER(19, 0, False), nullable=False),
    Column('lastmessageid', NUMBER(19, 0, False), nullable=False),
    Column('msgfrom', VARCHAR(32)),
    Column('msgto', VARCHAR(32)),
    schema='COCCDM'
)


t_mcm_contentlocation = Table(
    'mcm_contentlocation', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('name', VARCHAR(100)),
    schema='COCCDM'
)


t_mcm_criteriatype = Table(
    'mcm_criteriatype', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('name', VARCHAR(100)),
    Column('criteriaclassname', VARCHAR(500)),
    schema='COCCDM'
)


t_mcm_matchtype = Table(
    'mcm_matchtype', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('name', VARCHAR(250)),
    Column('matchtypelogicclass', VARCHAR(250)),
    schema='COCCDM'
)


t_mcm_promotion = Table(
    'mcm_promotion', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('name', VARCHAR(100)),
    Column('active', VARCHAR(5)),
    Column('contenttypeid', NUMBER(10, 0, False), nullable=False),
    Column('priority', NUMBER(10, 0, False), nullable=False),
    Column('startdate', DateTime),
    Column('enddate', DateTime),
    Column('matchtypeid', NUMBER(10, 0, False), nullable=False),
    Column('linktypeid', NUMBER(10, 0, False), nullable=False),
    Column('textcontent', Text),
    Column('imagecontentid', NUMBER(10, 0, False)),
    Column('linkurl', VARCHAR(500)),
    Column('linktarget', VARCHAR(50)),
    Column('usemessaging', VARCHAR(5)),
    Column('fulfillmenthostcommand', VARCHAR(255)),
    Column('fulfillmentdetails', Text),
    Column('alignment', VARCHAR(50)),
    Column('imageoptions', VARCHAR(250)),
    Column('personalizationenabled', VARCHAR(5)),
    Column('fulfillmentbuttonaccepttext', VARCHAR(50)),
    Column('fulfillmentbuttondeclinetext', VARCHAR(50)),
    Column('hideifalreadyaccepted', VARCHAR(5)),
    Column('personalizationhostcommandname', VARCHAR(100)),
    Column('fulfillacceptmessagequeuetext', VARCHAR(1000)),
    Column('oneclickfulfillment', VARCHAR(5)),
    Column('remindmelatertype', VARCHAR(25)),
    Column('remindmelaterunits', NUMBER(10, 0, False), nullable=False),
    Column('hideifalreadyrejected', VARCHAR(5)),
    Column('trackviews', VARCHAR(5)),
    Column('remindmelaterbuttontext', VARCHAR(50)),
    Column('messagequeueid', NUMBER(19, 0, False)),
    Column('facebookintegration', VARCHAR(5)),
    Column('facebooktitle', VARCHAR(500)),
    Column('facebookcontent', Text),
    Column('afteraccepturl', VARCHAR(500)),
    Column('title', VARCHAR(100)),
    Column('keywords', VARCHAR(500)),
    Column('rejecturl', VARCHAR(500)),
    Column('remindmelaterurl', VARCHAR(500)),
    Column('imagealttext', VARCHAR(255)),
    Column('isvendortype', VARCHAR(5)),
    schema='COCCDM'
)


t_mcm_promotionactivity = Table(
    'mcm_promotionactivity', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('promotionid', NUMBER(10, 0, False), nullable=False),
    Column('institutionuserid', VARCHAR(50)),
    Column('activitytype', NUMBER(10, 0, False), nullable=False),
    Column('activitydate', DateTime, nullable=False),
    Column('contentlocationid', NUMBER(10, 0, False)),
    Column('userid', VARCHAR(50)),
    schema='COCCDM'
)


t_mcm_promotionactivity_temp = Table(
    'mcm_promotionactivity_temp', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('promotionid', NUMBER(10, 0, False), nullable=False),
    Column('institutionuserid', VARCHAR(50)),
    Column('activitytype', NUMBER(10, 0, False), nullable=False),
    Column('activitydate', DateTime, nullable=False),
    Column('contentlocationid', NUMBER(10, 0, False)),
    Column('userid', VARCHAR(50)),
    schema='COCCDM'
)


t_mcm_promotioncontentlocation = Table(
    'mcm_promotioncontentlocation', Base.metadata,
    Column('promotionid', NUMBER(10, 0, False), nullable=False),
    Column('contentlocationid', NUMBER(10, 0, False), nullable=False),
    schema='COCCDM'
)


t_mcm_promotioncriteria = Table(
    'mcm_promotioncriteria', Base.metadata,
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('promotionid', NUMBER(10, 0, False), nullable=False),
    Column('criteriatypeid', NUMBER(10, 0, False), nullable=False),
    Column('criteriadata', Text),
    schema='COCCDM'
)


t_mcm_promotionpersonalization = Table(
    'mcm_promotionpersonalization', Base.metadata,
    Column('promotionid', NUMBER(10, 0, False), nullable=False),
    Column('institutionuserid', VARCHAR(50)),
    Column('customfield1', VARCHAR(500)),
    Column('customfield2', VARCHAR(500)),
    Column('customfield3', VARCHAR(500)),
    Column('customfield4', VARCHAR(500)),
    Column('customfield5', VARCHAR(500)),
    schema='COCCDM'
)


t_mcm_rpt_daily_promoactv = Table(
    'mcm_rpt_daily_promoactv', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('promotionid', NUMBER(10, 0, False), nullable=False),
    Column('institutionuserid', VARCHAR(50)),
    Column('activitytype', NUMBER(10, 0, False), nullable=False),
    Column('activitydate', DateTime, nullable=False),
    Column('contentlocationid', NUMBER(10, 0, False)),
    Column('activitycount', NUMBER(10, 0, False)),
    Column('id', NUMBER(19, 0, False)),
    schema='COCCDM'
)


t_mcm_rpt_daily_promoactv_temp = Table(
    'mcm_rpt_daily_promoactv_temp', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('promotionid', NUMBER(10, 0, False), nullable=False),
    Column('institutionuserid', VARCHAR(50)),
    Column('activitytype', NUMBER(10, 0, False), nullable=False),
    Column('activitydate', DateTime, nullable=False),
    Column('contentlocationid', NUMBER(10, 0, False)),
    Column('activitycount', NUMBER(10, 0, False)),
    Column('id', NUMBER(19, 0, False)),
    schema='COCCDM'
)


t_mcm_rpt_monthly_promoactv = Table(
    'mcm_rpt_monthly_promoactv', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('promotionid', NUMBER(10, 0, False), nullable=False),
    Column('institutionuserid', VARCHAR(50)),
    Column('activitytype', NUMBER(10, 0, False), nullable=False),
    Column('activitydate', DateTime, nullable=False),
    Column('contentlocationid', NUMBER(10, 0, False)),
    Column('activitycount', NUMBER(10, 0, False)),
    Column('id', NUMBER(19, 0, False)),
    schema='COCCDM'
)


t_mcm_rpt_yearly_promoactv = Table(
    'mcm_rpt_yearly_promoactv', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('promotionid', NUMBER(10, 0, False), nullable=False),
    Column('institutionuserid', VARCHAR(50)),
    Column('activitytype', NUMBER(10, 0, False), nullable=False),
    Column('activitydate', DateTime, nullable=False),
    Column('contentlocationid', NUMBER(10, 0, False)),
    Column('activitycount', NUMBER(10, 0, False)),
    Column('id', NUMBER(19, 0, False)),
    schema='COCCDM'
)


t_mcm_userlist = Table(
    'mcm_userlist', Base.metadata,
    Column('dataspace', VARCHAR(10)),
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('name', VARCHAR(50)),
    schema='COCCDM'
)


t_mcm_userlistdata = Table(
    'mcm_userlistdata', Base.metadata,
    Column('listid', NUMBER(10, 0, False), nullable=False),
    Column('institutionuserid', VARCHAR(50)),
    schema='COCCDM'
)


t_nc_notification_center = Table(
    'nc_notification_center', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('userid', VARCHAR(50)),
    Column('description', VARCHAR(500)),
    Column('priority', NUMBER(10, 0, False), nullable=False),
    Column('required', VARCHAR(5)),
    Column('actionlink', VARCHAR(200)),
    Column('type', VARCHAR(30)),
    Column('deletable', VARCHAR(5)),
    Column('insertdate', DateTime, nullable=False),
    Column('updatedate', DateTime),
    Column('deleted', VARCHAR(5)),
    schema='COCCDM'
)


t_ns_channeldestinations = Table(
    'ns_channeldestinations', Base.metadata,
    Column('channeldestid', NUMBER(10, 0, False), nullable=False),
    Column('subscchannelid', NUMBER(10, 0, False), nullable=False),
    Column('destinationaddress', NUMBER(10, 0, False), nullable=False),
    Column('deleted', VARCHAR(1)),
    schema='COCCDM'
)


t_ns_channels = Table(
    'ns_channels', Base.metadata,
    Column('channelid', NUMBER(10, 0, False), nullable=False),
    Column('typename', VARCHAR(255)),
    Column('name', VARCHAR(50)),
    Column('description', VARCHAR(255)),
    Column('enabled', VARCHAR(5)),
    Column('dataspace', VARCHAR(50)),
    Column('criteria', Text),
    Column('deleted', VARCHAR(1)),
    schema='COCCDM'
)


t_ns_deliveryqueue = Table(
    'ns_deliveryqueue', Base.metadata,
    Column('deliveryqueueid', NUMBER(10, 0, False), nullable=False),
    Column('notificationstring', Text),
    Column('subject', VARCHAR(255)),
    Column('destinationaddress', VARCHAR(200)),
    Column('subscriberid', NUMBER(10, 0, False)),
    Column('channelid', NUMBER(10, 0, False), nullable=False),
    Column('notificationtypeid', NUMBER(10, 0, False), nullable=False),
    Column('subscriptionid', NUMBER(10, 0, False)),
    Column('lastattempted', DateTime),
    Column('numberofattempts', NUMBER(10, 0, False)),
    Column('deliverydate', DateTime),
    Column('status', VARCHAR(20)),
    Column('ishtml', VARCHAR(5)),
    Column('errormessage', VARCHAR(500)),
    Column('createdate', DateTime, nullable=False),
    Column('dataspace', VARCHAR(50)),
    Column('subscriberchanneldata', Text),
    schema='COCCDM'
)


t_ns_deliveryqueue_temp = Table(
    'ns_deliveryqueue_temp', Base.metadata,
    Column('deliveryqueueid', NUMBER(10, 0, False), nullable=False),
    Column('notificationstring', Text),
    Column('subject', VARCHAR(255)),
    Column('destinationaddress', VARCHAR(200)),
    Column('subscriberid', NUMBER(10, 0, False)),
    Column('channelid', NUMBER(10, 0, False), nullable=False),
    Column('notificationtypeid', NUMBER(10, 0, False), nullable=False),
    Column('subscriptionid', NUMBER(10, 0, False)),
    Column('lastattempted', DateTime),
    Column('numberofattempts', NUMBER(10, 0, False)),
    Column('deliverydate', DateTime),
    Column('status', VARCHAR(20)),
    Column('ishtml', VARCHAR(5)),
    Column('errormessage', VARCHAR(500)),
    Column('createdate', DateTime, nullable=False),
    Column('dataspace', VARCHAR(50)),
    Column('subscriberchanneldata', Text),
    schema='COCCDM'
)


t_ns_errorlog = Table(
    'ns_errorlog', Base.metadata,
    Column('subscriberid', NUMBER(10, 0, False), nullable=False),
    Column('notificationtypeid', NUMBER(10, 0, False), nullable=False),
    Column('subscriptionid', NUMBER(10, 0, False)),
    Column('errormessage', VARCHAR(500)),
    Column('createdate', DateTime, nullable=False),
    Column('id', NUMBER(19, 0, False)),
    schema='COCCDM'
)


t_ns_errorlog_temp = Table(
    'ns_errorlog_temp', Base.metadata,
    Column('subscriberid', NUMBER(10, 0, False), nullable=False),
    Column('notificationtypeid', NUMBER(10, 0, False), nullable=False),
    Column('subscriptionid', NUMBER(10, 0, False)),
    Column('errormessage', VARCHAR(500)),
    Column('createdate', DateTime, nullable=False),
    Column('id', NUMBER(19, 0, False)),
    schema='COCCDM'
)


t_ns_notificationtype = Table(
    'ns_notificationtype', Base.metadata,
    Column('notificationtypeid', NUMBER(10, 0, False), nullable=False),
    Column('typename', VARCHAR(255)),
    Column('threshold', NUMBER(10, 0, False), nullable=False),
    Column('interval', NUMBER(10, 0, False), nullable=False),
    Column('notificationcriteria', Text),
    Column('dataspace', VARCHAR(50)),
    Column('deleted', VARCHAR(1)),
    Column('createdate', DateTime),
    Column('updatedate', DateTime),
    Column('deletedate', DateTime),
    schema='COCCDM'
)


t_ns_subscriber = Table(
    'ns_subscriber', Base.metadata,
    Column('subscriberid', NUMBER(10, 0, False), nullable=False),
    Column('userid', VARCHAR(50)),
    Column('dataspace', VARCHAR(50)),
    Column('preferredculture', VARCHAR(20)),
    schema='COCCDM'
)


t_ns_subscriberchanneldest = Table(
    'ns_subscriberchanneldest', Base.metadata,
    Column('subscriberchanneldestid', NUMBER(10, 0, False), nullable=False),
    Column('subcriberid', NUMBER(10, 0, False), nullable=False),
    Column('channelid', NUMBER(10, 0, False), nullable=False),
    Column('destinationaddress', VARCHAR(255)),
    Column('criteria', Text),
    Column('deleted', VARCHAR(1)),
    schema='COCCDM'
)


t_ns_subscription = Table(
    'ns_subscription', Base.metadata,
    Column('subscriptionid', NUMBER(10, 0, False), nullable=False),
    Column('notificationtypeid', NUMBER(10, 0, False), nullable=False),
    Column('subscriberid', NUMBER(10, 0, False), nullable=False),
    Column('subscriptioncriteria', Text),
    Column('deleted', VARCHAR(1)),
    Column('createdate', DateTime, nullable=False),
    Column('updatedate', DateTime),
    Column('deletedate', DateTime),
    Column('status', NUMBER(3, 0, False), nullable=False),
    Column('faileddate', DateTime),
    Column('owneruserid', VARCHAR(60)),
    schema='COCCDM'
)


t_ns_subscriptionchannel = Table(
    'ns_subscriptionchannel', Base.metadata,
    Column('subscchannelid', NUMBER(10, 0, False), nullable=False),
    Column('subscriptionid', NUMBER(10, 0, False), nullable=False),
    Column('channelid', NUMBER(10, 0, False), nullable=False),
    Column('deleted', VARCHAR(1)),
    schema='COCCDM'
)


class Org(Base):
    __tablename__ = 'org'
    __table_args__ = (
        PrimaryKeyConstraint('orgnbr', name='pk_org'),
        {'schema': 'COCCDM'}
    )

    orgnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    orgname: Mapped[str] = mapped_column(VARCHAR(60))
    validyn: Mapped[str] = mapped_column(CHAR(1))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    rpt1099intyn: Mapped[str] = mapped_column(CHAR(1))
    privacyyn: Mapped[str] = mapped_column(CHAR(1))
    taxexemptyn: Mapped[str] = mapped_column(CHAR(1))
    purgeyn: Mapped[str] = mapped_column(CHAR(1))
    swiftbranchyn: Mapped[str] = mapped_column(VARCHAR(1))
    parentorgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    orgnamesndx: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    orgtypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    currroutenbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    adddate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    frgncertexpdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    mailtypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    swiftaddr: Mapped[Optional[str]] = mapped_column(VARCHAR(11))


class Orgaddruse(Base):
    __tablename__ = 'orgaddruse'
    __table_args__ = (
        PrimaryKeyConstraint('orgnbr', 'addrusecd', name='pk_orgaddruse'),
        {'schema': 'COCCDM'}
    )

    orgnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    addrusecd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    addrnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    startdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    stopdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    inactivedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    effdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    occupancydate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    startmonthcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    startdaynbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    stopmonthcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    stopdaynbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))


class Orgphone(Base):
    __tablename__ = 'orgphone'
    __table_args__ = (
        PrimaryKeyConstraint('orgnbr', 'phoneusecd', 'phoneseq', name='pk_orgphone'),
        {'schema': 'COCCDM'}
    )

    orgnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Organization Number is part of the primary key and is a foreign key to the Organization Table.')
    phoneusecd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True, comment='The Phone Use Code is part of the primary key and is a foreign key to the Phone Use Table.')
    phoneseq: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Phone Sequence is part of the primary key and is system assigned.')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM  USE  ONLY.')
    ctrycd: Mapped[str] = mapped_column(VARCHAR(4), server_default=text("'USA' "), comment='The Country Code Column Identifies the code for the country.')
    areacd: Mapped[Optional[str]] = mapped_column(VARCHAR(5), comment='The Area Code is the 3 digit area code for the phone number.')
    exchange: Mapped[Optional[str]] = mapped_column(VARCHAR(3), comment='The Exchange is the 3 digit exchange part of the phone number.')
    phonenbr: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The Phone Number is the 4 digit phone number.')
    phoneexten: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The Phone Extension is the extension for the phone number.')
    foreignphonenbr: Mapped[Optional[str]] = mapped_column(VARCHAR(10), comment='The Foreign Phone Number column is the the 10 digit foreign phone number.')
    preferredyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1), comment='Determines the preferred phone number to use.')


class Orgtaxid(Base):
    __tablename__ = 'orgtaxid'
    __table_args__ = (
        PrimaryKeyConstraint('orgnbr', 'taxidtypcd', name='pk_orgtaxid'),
        {'schema': 'COCCDM'}
    )

    orgnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    taxidtypcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    taxid: Mapped[Optional[str]] = mapped_column(VARCHAR(60))
    certdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    applydate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class Orguserfield(Base):
    __tablename__ = 'orguserfield'
    __table_args__ = (
        PrimaryKeyConstraint('orgnbr', 'userfieldcd', name='pk_orguserfield'),
        {'schema': 'COCCDM'}
    )

    orgnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    userfieldcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    value: Mapped[Optional[str]] = mapped_column(VARCHAR(254))


class Orgwrn(Base):
    __tablename__ = 'orgwrn'
    __table_args__ = (
        PrimaryKeyConstraint('orgnbr', 'effdate', 'wrnflagcd', name='pk_orgwrn'),
        {'schema': 'COCCDM'}
    )

    orgnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Organization Number is the system-assigned number that uniquely identifies each organization.')
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True, comment='The effective date is the date when the organization warning flag goes into effect.')
    wrnflagcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True, comment='The Warning Flag Code is the user-assigned code used to uniquely identify the warning.')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='The Date Last Maintenance is The date when this row was most recently updated. SYSTEM USE ONLY.')
    notenbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The note number is the system-assigned number that uniquely identifies the note associated with this organization warning flag.')
    inactivedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The Inactive date is the date when this organization warning flag is no longer in effect.')


class Pers(Base):
    __tablename__ = 'pers'
    __table_args__ = (
        PrimaryKeyConstraint('persnbr', name='pk_pers'),
        {'schema': 'COCCDM'}
    )

    persnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    restaxctrycd: Mapped[str] = mapped_column(VARCHAR(4))
    lastname: Mapped[str] = mapped_column(VARCHAR(20))
    firstname: Mapped[str] = mapped_column(VARCHAR(20))
    adddate: Mapped[datetime.datetime] = mapped_column(DateTime)
    validyn: Mapped[str] = mapped_column(VARCHAR(1))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    rpt1042syn: Mapped[str] = mapped_column(CHAR(1))
    privacyyn: Mapped[str] = mapped_column(CHAR(1))
    purgeyn: Mapped[str] = mapped_column(CHAR(1))
    spousepersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    crcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    salucd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    lastnamesndx: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    firstnamesndx: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    mdlinit: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    mdlname: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    nickname: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    suffix: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    taxid: Mapped[Optional[str]] = mapped_column(VARCHAR(60))
    datebirth: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datedeath: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datetaxidapply: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datetaxcert: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    educlevcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    incomelevcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    nbrdepnd: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    occptncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    mailtypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    ownrent: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    custkeyword: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    frgncertexpdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    lastnameupper: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    firstnameupper: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    graddate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    creditreportconsinfocd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    shortname: Mapped[Optional[str]] = mapped_column(VARCHAR(2))


class Persaddruse(Base):
    __tablename__ = 'persaddruse'
    __table_args__ = (
        PrimaryKeyConstraint('persnbr', 'addrusecd', name='pk_persaddruse'),
        {'schema': 'COCCDM'}
    )

    persnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    addrusecd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    addrnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False))
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    startdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    stopdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    inactivedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    occupancydate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    startmonthcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    startdaynbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    stopmonthcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    stopdaynbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))


class Persempl(Base):
    __tablename__ = 'persempl'
    __table_args__ = (
        PrimaryKeyConstraint('persnbr', name='pk_persempl'),
        {'schema': 'COCCDM'}
    )

    persnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Person Number is the system assigned number that identifies each person.')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM  USE  ONLY.')
    effdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The Effective Date is the date the person was added as a employee.')
    inactivedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The Inactive Date is the date the person is no longer an employee.')
    mincashboxamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='The Minimum cashbox amount.')
    maxcashboxamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='The Maximum cashbox amount.')
    maxcheckcashamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='The Maximum Check cash amount.')
    maxcashwithdrawamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='The Maximum Cash withdrawal amount.')
    maxcashbackamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='The Maximum Cash back amount.')
    lendlimitamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True), comment='The Lend Limit amount.')


class Persid(Base):
    __tablename__ = 'persid'
    __table_args__ = (
        PrimaryKeyConstraint('persnbr', 'persidtypcd', name='pk_persid'),
        {'schema': 'COCCDM'}
    )

    persnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    persidtypcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    ctrycd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    statecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    idnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    issuer: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    issuedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    comments: Mapped[Optional[str]] = mapped_column(VARCHAR(300))
    expiredate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ctrysubdivcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))


class Persidtyp(Base):
    __tablename__ = 'persidtyp'
    __table_args__ = (
        PrimaryKeyConstraint('persidtypcd', name='pk_persidtyp'),
        {'schema': 'COCCDM'}
    )

    persidtypcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    persidtypdesc: Mapped[str] = mapped_column(VARCHAR(30))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    desctokennbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    descnamespacecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))


class Persuserfield(Base):
    __tablename__ = 'persuserfield'
    __table_args__ = (
        PrimaryKeyConstraint('persnbr', 'userfieldcd', name='pk_persuserfield'),
        {'schema': 'COCCDM'}
    )

    persnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    userfieldcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    value: Mapped[Optional[str]] = mapped_column(VARCHAR(254))


class Perswrn(Base):
    __tablename__ = 'perswrn'
    __table_args__ = (
        PrimaryKeyConstraint('persnbr', 'effdate', 'wrnflagcd', name='pk_perswrn'),
        {'schema': 'COCCDM'}
    )

    persnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The system assigned number for the person.')
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True, comment='The effective date of the person warning flag.')
    wrnflagcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True, comment='The Warning Flag Code is the code used to idenfity the warning.')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM USE ONLY.')
    notenbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The note number associated with this person warning flag.')
    inactivedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The date the person warning flag goes inactive.')


t_prof_profilesettings = Table(
    'prof_profilesettings', Base.metadata,
    Column('autoid', NUMBER(10, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('groupname', VARCHAR(50)),
    Column('userid', VARCHAR(50)),
    Column('settingkey', VARCHAR(50)),
    Column('settingtype', VARCHAR(250)),
    Column('settingvalue', VARCHAR(2000)),
    schema='COCCDM'
)


class Profitprofile(Base):
    __tablename__ = 'profitprofile'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'processdate', name='pk_profitprofile'),
        {'comment': 'Profit Profile table in Datamart database', 'schema': 'COCCDM'}
    )

    finbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), comment='FI Number')
    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='Account Number')
    processdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True, comment='Process Date')
    monthendyn: Mapped[str] = mapped_column(VARCHAR(1), server_default=text("'N' "), comment='Is Month End')
    owneroverrideyn: Mapped[str] = mapped_column(VARCHAR(1), server_default=text("'N' "), comment='Is Tax Owner being Overriden')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='Last date and time the row was changed (inserted or updated).')
    persnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Person Number')
    orgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Orgnization Number')
    notebal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Balance Amount')
    ftp: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Earnings Rate for Deposits. Funding Rate for Loans.')
    netinterestincome: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Net Interest Income')
    noninterestincome: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Non-Interest Income')
    noninterestexpense: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Non-Interest Expense')
    provisionexpense: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Provision Expense')
    annualprofit: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Annual Profit')
    totalprofit: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Total Profit')
    acctholdergrade: Mapped[Optional[str]] = mapped_column(VARCHAR(1), comment='Account Holder Grade')


class ProfitprofileTemp(Base):
    __tablename__ = 'profitprofile_temp'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'processdate', name='pk_profitprofile_temp'),
        {'comment': 'Profit Profile Temp table in Datamart database',
     'schema': 'COCCDM'}
    )

    finbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), comment='FI Number')
    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='Account Number')
    processdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True, comment='Process Date')
    monthendyn: Mapped[str] = mapped_column(VARCHAR(1), server_default=text("'N' "), comment='Is Month End')
    owneroverrideyn: Mapped[str] = mapped_column(VARCHAR(1), server_default=text("'N' "), comment='Is Tax Owner being Overriden')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='Last date and time the row was changed (inserted or updated).')
    persnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Person Number')
    orgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Orgnization Number')
    notebal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Balance Amount')
    ftp: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Earnings Rate for Deposits. Funding Rate for Loans.')
    netinterestincome: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Net Interest Income')
    noninterestincome: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Non-Interest Income')
    noninterestexpense: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Non-Interest Expense')
    provisionexpense: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Provision Expense')
    annualprofit: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Annual Profit')
    totalprofit: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True), comment='Total Profit')
    acctholdergrade: Mapped[Optional[str]] = mapped_column(VARCHAR(1), comment='Account Holder Grade')


class Propuserfield(Base):
    __tablename__ = 'propuserfield'
    __table_args__ = (
        PrimaryKeyConstraint('propnbr', 'userfieldcd', name='pk_propuserfield'),
        {'schema': 'COCCDM'}
    )

    propnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    userfieldcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    value: Mapped[Optional[str]] = mapped_column(VARCHAR(254))


t_pups_personalizedportalpage = Table(
    'pups_personalizedportalpage', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('pageid', VARCHAR(256)),
    Column('moduleid', VARCHAR(256)),
    Column('show', VARCHAR(5)),
    Column('expanded', VARCHAR(5)),
    Column('dockid', VARCHAR(256)),
    Column('orderindock', NUMBER(10, 0, False), nullable=False),
    Column('dateinserted', DateTime, nullable=False),
    Column('dateupdated', DateTime, nullable=False),
    schema='COCCDM'
)


t_pups_portalusersettings = Table(
    'pups_portalusersettings', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('inuserpersonalizationmode', VARCHAR(5)),
    Column('dateinserted', DateTime, nullable=False),
    Column('dateupdated', DateTime, nullable=False),
    schema='COCCDM'
)


t_rp_linkedrole = Table(
    'rp_linkedrole', Base.metadata,
    Column('providerkey', VARCHAR(20)),
    Column('parentroleid', NUMBER(10, 0, False), nullable=False),
    Column('childroleid', NUMBER(10, 0, False), nullable=False),
    Column('directlink', VARCHAR(5)),
    schema='COCCDM'
)


t_rp_role = Table(
    'rp_role', Base.metadata,
    Column('providerkey', VARCHAR(20)),
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('name', VARCHAR(50)),
    Column('category', VARCHAR(100)),
    Column('description', VARCHAR(100)),
    Column('hidden', VARCHAR(5)),
    schema='COCCDM'
)


t_rp_userrole = Table(
    'rp_userrole', Base.metadata,
    Column('providerkey', VARCHAR(20)),
    Column('dataspace', VARCHAR(10)),
    Column('userid', VARCHAR(32)),
    Column('roleid', NUMBER(10, 0, False), nullable=False),
    schema='COCCDM'
)


t_sf_formcategory = Table(
    'sf_formcategory', Base.metadata,
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('formcategory', VARCHAR(100)),
    schema='COCCDM'
)


t_sf_secureform = Table(
    'sf_secureform', Base.metadata,
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('formname', VARCHAR(32)),
    Column('formtitle', VARCHAR(100)),
    Column('formdescription', VARCHAR(255)),
    Column('formcategoryid', NUMBER(10, 0, False)),
    Column('destinationcategoryid', NUMBER(10, 0, False), nullable=False),
    Column('rightalignlabels', VARCHAR(5)),
    Column('rightcssclass', VARCHAR(20)),
    Column('prepopulationproviderguid', VARCHAR(39)),
    Column('createsecuremessage', VARCHAR(5)),
    Column('roles', Text),
    Column('submitbuttontext', VARCHAR(50)),
    Column('cancelbuttontext', VARCHAR(50)),
    Column('formlayouttemplate', Text),
    Column('messagelayouttemplate', Text),
    Column('active', VARCHAR(5)),
    Column('fieldxml', Text),
    Column('createdateutc', DateTime, nullable=False),
    Column('updatedateutc', DateTime, nullable=False),
    Column('updatedby', VARCHAR(32)),
    Column('deleted', VARCHAR(5)),
    schema='COCCDM'
)


t_sf_userfielddata = Table(
    'sf_userfielddata', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('formdataid', NUMBER(19, 0, False), nullable=False),
    Column('fieldname', VARCHAR(32)),
    Column('fieldvalue', VARCHAR(128)),
    Column('fieldtext', Text),
    Column('fieldorder', NUMBER(10, 0, False), nullable=False),
    schema='COCCDM'
)


t_sf_userformdata = Table(
    'sf_userformdata', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('formid', NUMBER(10, 0, False), nullable=False),
    Column('userid', NUMBER(10, 0, False), nullable=False),
    Column('createdateutc', DateTime, nullable=False),
    Column('updatedby', VARCHAR(32)),
    schema='COCCDM'
)


t_sms_mobilenickname = Table(
    'sms_mobilenickname', Base.metadata,
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('accountid', VARCHAR(64)),
    Column('mobilenickname', VARCHAR(10)),
    Column('enabledflag', VARCHAR(5)),
    Column('primaryflag', VARCHAR(5)),
    Column('insertdateutc', DateTime, nullable=False),
    schema='COCCDM'
)


t_sms_phonenumber = Table(
    'sms_phonenumber', Base.metadata,
    Column('phonenumberid', NUMBER(19, 0, False), nullable=False),
    Column('phonenumber', VARCHAR(24)),
    Column('userid', NUMBER(19, 0, False), nullable=False),
    Column('statusid', NUMBER(3, 0, False), nullable=False),
    Column('channelid', NUMBER(3, 0, False), nullable=False),
    Column('updatedateutc', DateTime, nullable=False),
    Column('receivecount', NUMBER(10, 0, False), nullable=False),
    Column('lastreceivedateutc', DateTime),
    schema='COCCDM'
)


t_sms_phonestatus = Table(
    'sms_phonestatus', Base.metadata,
    Column('statusid', NUMBER(3, 0, False), nullable=False),
    Column('statusname', VARCHAR(32)),
    schema='COCCDM'
)


t_users = Table(
    'users', Base.metadata,
    Column('username', VARCHAR(128), nullable=False),
    Column('user_id', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    schema='COCCDM'
)


t_view_wh_acctuserfields = Table(
    'view_wh_acctuserfields', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False),
    Column('1098_Mortgage_Acquisition_MADT', VARCHAR(254)),
    Column('1st_Preferred_Ship_Mortga_SHIP', VARCHAR(254)),
    Column('ATM/POS_Opt_In_Flag_REOD', VARCHAR(254)),
    Column('Affordable_Units_AFFU', VARCHAR(254)),
    Column('Associated_Party_ASPA', VARCHAR(254)),
    Column('BancVue_BVUE', VARCHAR(254)),
    Column('CDARS_Customer_CDAR', VARCHAR(254)),
    Column('CML_Loan_Secured_by_Resid_CSBR', VARCHAR(254)),
    Column('CML_Policy_Exception_1st_CME1', VARCHAR(254)),
    Column('CML_Policy_Exception_2nd_CME2', VARCHAR(254)),
    Column('CML_Policy_Exception_3rd_CME3', VARCHAR(254)),
    Column('COCC_Prepayment_Penalty_E_CPPD', VARCHAR(254)),
    Column('COVID-19_Impacted_CV19', VARCHAR(254)),
    Column('COVID_Defer_#_Months_CV03', VARCHAR(254)),
    Column('COVID_Defer_Esc_Pmt_YN_CV05', VARCHAR(254)),
    Column('COVID_Deferred_Payment_YN_CV01', VARCHAR(254)),
    Column('COVID_Deferred_Start_Date_CV02', VARCHAR(254)),
    Column('COVID_Repayment_#_Months_CV04', VARCHAR(254)),
    Column('COVID_Repayment_Option_CV06', VARCHAR(254)),
    Column('CT_Deal_Num_CTDN', VARCHAR(254)),
    Column('CT_Entity_Num_CTEN', VARCHAR(254)),
    Column('Centrix_Positive_Pay_CAPP', VARCHAR(254)),
    Column('Closing_Attorney_CLAT', VARCHAR(254)),
    Column('Communication_Method_ODCM', VARCHAR(254)),
    Column('Community_Dev_Loan_CDL', VARCHAR(254)),
    Column('Consumer_Loan_Purpose_CLNP', VARCHAR(254)),
    Column('Covid_Exception_Descripti_EXC1', VARCHAR(254)),
    Column('Covid_Exception_Descripti_EXC2', VARCHAR(254)),
    Column('Covid_Exception_Descripti_EXC3', VARCHAR(254)),
    Column('Credit_Score_Borrower_2_CRS2', VARCHAR(254)),
    Column('Credit_Score_Borrower_3_CRS3', VARCHAR(254)),
    Column('Credit_Score_Borrower_4_CRS4', VARCHAR(254)),
    Column('Credit_Score_CRSC', VARCHAR(254)),
    Column('Dealer_Name_DLR', VARCHAR(254)),
    Column('Dealer_Portal_ID_DLID', VARCHAR(254)),
    Column('Dealer_Split_Rate_SPLT', VARCHAR(254)),
    Column('Deferred_Interest_Credit_CV08', VARCHAR(254)),
    Column('Digital_Document_DDOC', VARCHAR(254)),
    Column('Digital_Document_Print_Op_PDOC', VARCHAR(254)),
    Column('Discharge_Date_DCDT', VARCHAR(254)),
    Column('Discharge_Sent_To_DCSE', VARCHAR(254)),
    Column('EBL_Fee_EBLF', VARCHAR(254)),
    Column('E_Contract_ECON', VARCHAR(254)),
    Column('Extension_Modification_Da_EXMD', VARCHAR(254)),
    Column('FDM_Date_TDAT', VARCHAR(254)),
    Column('FDM_Note_TNOT', VARCHAR(254)),
    Column('fdm_y_n_tdr', VARCHAR(254)),
    Column('FNB_-_Converted_Loan_FNBL', VARCHAR(254)),
    Column('First_Time_Homebuyer_FTHB', VARCHAR(254)),
    Column('Fund_Program_FDPM', VARCHAR(254)),
    Column('Gross_Annual_Stated_Reven_GASR', VARCHAR(254)),
    Column('HELOC_in_Repayment_RPAY', VARCHAR(254)),
    Column('High_Volatility_Loan_HIGH', VARCHAR(254)),
    Column('In_Repayment_YN_CV07', VARCHAR(254)),
    Column('Income_INCO', VARCHAR(254)),
    Column('Line_of_Credit_Type_LOCT', VARCHAR(254)),
    Column('Loan_Impaired_IMPL', VARCHAR(254)),
    Column('Loan_Restructured_REST', VARCHAR(254)),
    Column('Low_to_Moderate_Income_LMI', VARCHAR(254)),
    Column('Mass_Small_Business_Banki_MSBP', VARCHAR(254)),
    Column('Military_Lending_Act_MLA', VARCHAR(254)),
    Column('Minority_Owned_MIOW', VARCHAR(254)),
    Column('NEF-AHP_Rpt_End_Date_PRED', VARCHAR(254)),
    Column('Never_Print_NDOC', VARCHAR(254)),
    Column('New_CML_Loan_Money_NCML', VARCHAR(254)),
    Column('Non-Recourse_NREC', VARCHAR(254)),
    Column('Non_Owner_Occupied_Constr_NOOC', VARCHAR(254)),
    Column('ODP_Status_Code_ODP', VARCHAR(254)),
    Column('Opt_Out_of_Skip_A_Pay_OOSP', VARCHAR(254)),
    Column('Origination_Branch_BRNC', VARCHAR(254)),
    Column('Origination_Channel_ORCH', VARCHAR(254)),
    Column('PMI_Year_End_Reportable_PMYE', VARCHAR(254)),
    Column('PNC_ID_Number_PNC', VARCHAR(254)),
    Column('Participation_%_purchased_PAPU', VARCHAR(254)),
    Column('Participation_Purchased_PARP', VARCHAR(254)),
    Column('Participation_Sold_FPTS', VARCHAR(254)),
    Column('Pledged_Collateral_PLED', VARCHAR(254)),
    Column('Portfolio_Key_HHNU', VARCHAR(254)),
    Column('Positive_Pay_Serial_Valid_PPSV', VARCHAR(254)),
    Column('Privacy_Act_Data_Shared_PRVC', VARCHAR(254)),
    Column('Product_Number_PROD', VARCHAR(254)),
    Column('Promo_Code_PRCO', VARCHAR(254)),
    Column('QC_Review_Date_QCRD', VARCHAR(254)),
    Column('QC_Reviewer_QCRV', VARCHAR(254)),
    Column('Qualified_Mortgage_QUAL', VARCHAR(254)),
    Column('Release_Type_RLTP', VARCHAR(254)),
    Column('sba_504_sba5', VARCHAR(254)),
    Column('SBA_Approval_Date_SBAA', VARCHAR(254)),
    Column('SBA_Fee_Yes/No_SBAF', VARCHAR(254)),
    Column('SBA_Guarantee_Expiration_SBGD', VARCHAR(254)),
    Column('SBA_Guarantee_Percent_SBAG', VARCHAR(254)),
    Column('SBA_Status_Code_Eff_Date_SBSD', VARCHAR(254)),
    Column('SBA_Status_Code_SBAS', VARCHAR(254)),
    Column('SWAP_Fixed_Interest_Rate_SWFR', VARCHAR(254)),
    Column('Service_Member_Civil_Reli_SCRA', VARCHAR(254)),
    Column('Site_Visit_Date_SVDT', VARCHAR(254)),
    Column('Site_Vist_Type_SVTY', VARCHAR(254)),
    Column('Swap_Maturity_SWMA', VARCHAR(254)),
    Column('Test_deposit_account_TDAC', VARCHAR(254)),
    Column('ucc_ucc', VARCHAR(254)),
    Column('Withholding_Status_WITH', VARCHAR(254)),
    Column('XAA_Account_XAA', VARCHAR(254)),
    schema='COCCDM'
)


t_view_wh_orguserfields = Table(
    'view_wh_orguserfields', Base.metadata,
    Column('orgnbr', NUMBER(22, 0, False), nullable=False),
    Column('ATM_Owner_VFAT', VARCHAR(254)),
    Column('Bankruptcy_BANK', VARCHAR(254)),
    Column('Bus_Online_Banking_ONLI', VARCHAR(254)),
    Column('CCM_-_Last_History_DateTi_CHIS', VARCHAR(254)),
    Column('CDARS_Customer_CDAR', VARCHAR(254)),
    Column('CIP_External_Verification_CIPV', VARCHAR(254)),
    Column('Credit_Card_Match_Process_6CCP', VARCHAR(254)),
    Column('DO_NOT_USE_CSC_Start_Dt_CCSD', VARCHAR(254)),
    Column('External_CLO_Review_COBB', VARCHAR(254)),
    Column('FNB_Acquired_Customer_FNBC', VARCHAR(254)),
    Column('FNB_Shared_Customer_FNBS', VARCHAR(254)),
    Column('Investment_Customer_INVI', VARCHAR(254)),
    Column('Marketing_Unsubscribe_Ema_MEMA', VARCHAR(254)),
    Column('Money_Services_Business_VFMS', VARCHAR(254)),
    Column('Nbr_of_Properties/Disburs_NODA', VARCHAR(254)),
    Column('New_Money_NEWM', VARCHAR(254)),
    Column('Next_Review_Date_NRD', VARCHAR(254)),
    Column('No_Email_Address_NOEM', VARCHAR(254)),
    Column('Non_Profit_Organization_NP', VARCHAR(254)),
    Column('Opt_Out_Affiliates_OPTF', VARCHAR(254)),
    Column('Opt_Out_BCSB_OPTB', VARCHAR(254)),
    Column('ptt_mem1_pttm', VARCHAR(254)),
    Column('Prime_Time_Deposit_PRTD', VARCHAR(254)),
    schema='COCCDM'
)


t_view_wh_persuserfields = Table(
    'view_wh_persuserfields', Base.metadata,
    Column('persnbr', NUMBER(22, 0, False), nullable=False),
    Column('ATM_Owner_VFAT', VARCHAR(254)),
    Column('Associated_Party_2_ASPY', VARCHAR(254)),
    Column('Authentication_Code_AUTC', VARCHAR(254)),
    Column('Authentication_Code_Hint_AUTH', VARCHAR(254)),
    Column('Bank_At_Work_BKAW', VARCHAR(254)),
    Column('Bankruptcy_BANK', VARCHAR(254)),
    Column('Bus_Online_Banking_ONLI', VARCHAR(254)),
    Column('CDARS_Customer_CDAR', VARCHAR(254)),
    Column('CIP_External_Verification_CIPV', VARCHAR(254)),
    Column('COVID-19_Impacted_CV19', VARCHAR(254)),
    Column('Confirm/Verified_Address_CAD8', VARCHAR(254)),
    Column('Cons_Credit_Card_App_CCCP', VARCHAR(254)),
    Column('Cons_Credit_Card_Approved_CCCR', VARCHAR(254)),
    Column('Credit_Refresh_CRRE', VARCHAR(254)),
    Column('Deceased_DECD', VARCHAR(254)),
    Column('Employer-EMPL_EMPL', VARCHAR(254)),
    Column('Employer_EMP', VARCHAR(254)),
    Column('External_CLO_Review_COBB', VARCHAR(254)),
    Column('FNB_Acquired_Customer_FNBC', VARCHAR(254)),
    Column('FNB_Shared_Customer_FNBS', VARCHAR(254)),
    Column('Foreign_TIN_FTIN', VARCHAR(254)),
    Column('How_did_you_hear_about_us_HDHU', VARCHAR(254)),
    Column('IDV_Results_IRST', VARCHAR(254)),
    Column('Investment_Customer_INVI', VARCHAR(254)),
    Column('KBA_Results_KRST', VARCHAR(254)),
    Column('Marketing_Unsubscribe_Ema_MEMA', VARCHAR(254)),
    Column('Marketing_Unsubscribe_SMS_MSMS', VARCHAR(254)),
    Column('Merchant_Pro_MERC', VARCHAR(254)),
    Column('Military_Active_End_Date_MAED', VARCHAR(254)),
    Column('Military_Active_Start_Dat_MASD', VARCHAR(254)),
    Column('Mobile_Baking_MOBB', VARCHAR(254)),
    Column('Money_Services_Business_VFMS', VARCHAR(254)),
    Column('New_Money_NEWM', VARCHAR(254)),
    Column('Next_Review_Date_NRD', VARCHAR(254)),
    Column('No_Email_Address_NOEM', VARCHAR(254)),
    Column('Occupation_Detail_OCCU', VARCHAR(254)),
    Column('Opt_Out_Affiliates_OPTF', VARCHAR(254)),
    Column('Opt_Out_BCSB_OPTB', VARCHAR(254)),
    Column('ptt_mem1_pttm', VARCHAR(254)),
    Column('PT_Travel_PTTR', VARCHAR(254)),
    Column('Person/Organization__ATM_6PFR', VARCHAR(254)),
    Column('Politically_Exposed_Perso_VFPE', VARCHAR(254)),
    Column('Positive_Pay_POSP', VARCHAR(254)),
    Column('Prime_Time_Deposit_PRTD', VARCHAR(254)),
    Column('Qualifile_Results_QRST', VARCHAR(254)),
    Column('Remote_Deposit_Capture_REDC', VARCHAR(254)),
    schema='COCCDM'
)


t_view_wh_propuserfields = Table(
    'view_wh_propuserfields', Base.metadata,
    Column('propnbr', NUMBER(22, 0, False), nullable=False),
    Column('PMI_Cancellation_Date_PMIB', VARCHAR(254)),
    Column('PMI_Half-Life_Date_PMIH', VARCHAR(254)),
    Column('PMI_Termination_Date_PMIT', VARCHAR(254)),
    schema='COCCDM'
)


class WhAcct(Base):
    __tablename__ = 'wh_acct'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rundate', name='wh_acct_pk'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    stmtacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    taxrptforownyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    taxrptforsigyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    retirementyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    mjaccttypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    currmiaccttypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    curracctstatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    mailtypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    mailaddrusecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    openfundsourcecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    owncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    datelastcontact: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datemat: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    taxrptfororgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    taxrptforpersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    branchorgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    nextrtxnnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    closereasoncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    passbookyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    acctdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    addrformatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    rpt1098yn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    rptptsyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    currterm: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    contractdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    transactionacctyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    stmtacctyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    truncateyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    analysisyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    maxoverdraftlimit: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    addrformatdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    privacyind: Mapped[Optional[str]] = mapped_column(CHAR(1))
    checksyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    checkimageyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    naicsnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The naicsnbr is the user assigned code that identifies the north American industry classification for a person.')
    naicstypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The naics type code is the code used to identify the hierarchical industry group in which each naicscd resides.')
    naicscd: Mapped[Optional[str]] = mapped_column(VARCHAR(6), comment='The government assigned naics industry class code.')
    naicsdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(254), comment='The government assigned naics industry description.')
    siccd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The sic code is the user assigned code that identifies the standard industrial class for a person.')
    sicdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(60), comment='The sic code is the user assigned code that identifies the valid standard industrial class used.')
    sicsubcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The sicsubcd is a user assigned code that identifies the standard industrial class sub that applies to a person. The sicsubcd is a user assigned code that identifies the standard industrial class sub that applies to a person.')
    sicsubdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(60), comment='The sic subordinate description is the textual description of the standard industry class subordinate codes.')
    creditscore: Mapped[Optional[float]] = mapped_column(NUMBER(15, 0, False))
    scoredate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    regeoptin: Mapped[Optional[str]] = mapped_column(VARCHAR(254))
    opendate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    addrnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Address Number is the system assigned number that uniquely identifies each address.')


class WhAcctMe(Base):
    __tablename__ = 'wh_acct_me'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rundate', name='sys_c_snap$_2wh_acct_temp_pk'),
        Index('wh_acct_me_dx1', 'curracctstatcd', 'mjaccttypcd', 'currmiaccttypcd'),
        Index('wh_acct_me_dx10', 'closereasoncd'),
        Index('wh_acct_me_dx11', 'addrformatcd'),
        Index('wh_acct_me_dx12', 'naicstypcd'),
        Index('wh_acct_me_dx13', 'naicscd'),
        Index('wh_acct_me_dx14', 'siccd'),
        Index('wh_acct_me_dx15', 'sicsubcd'),
        Index('wh_acct_me_dx16', 'acctnbr'),
        Index('wh_acct_me_dx2', 'mjaccttypcd', 'currmiaccttypcd'),
        Index('wh_acct_me_dx3', 'taxrptfororgnbr'),
        Index('wh_acct_me_dx4', 'taxrptforpersnbr'),
        Index('wh_acct_me_dx5', 'branchorgnbr'),
        Index('wh_acct_me_dx6', 'mailtypcd'),
        Index('wh_acct_me_dx7', 'mailaddrusecd'),
        Index('wh_acct_me_dx8', 'openfundsourcecd'),
        Index('wh_acct_me_dx9', 'owncd'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    stmtacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    taxrptforownyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    taxrptforsigyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    retirementyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    mjaccttypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    currmiaccttypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    curracctstatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    mailtypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    mailaddrusecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    openfundsourcecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    owncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    datelastcontact: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datemat: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    taxrptfororgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    taxrptforpersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    branchorgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    nextrtxnnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    closereasoncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    passbookyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    acctdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    addrformatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    rpt1098yn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    rptptsyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    currterm: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    contractdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    transactionacctyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    stmtacctyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    truncateyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    analysisyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    maxoverdraftlimit: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    addrformatdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    privacyind: Mapped[Optional[str]] = mapped_column(CHAR(1))
    checksyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    checkimageyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    naicsnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    naicstypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    naicscd: Mapped[Optional[str]] = mapped_column(VARCHAR(6))
    naicsdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(254))
    siccd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    sicdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(60))
    sicsubcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    sicsubdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(60))
    creditscore: Mapped[Optional[float]] = mapped_column(NUMBER(15, 0, False))
    scoredate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    regeoptin: Mapped[Optional[str]] = mapped_column(VARCHAR(254))
    opendate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    addrnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))


class WhAcctTemp(Base):
    __tablename__ = 'wh_acct_temp'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rundate', name='wh_acct_temp_pk'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    stmtacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    taxrptforownyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    taxrptforsigyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    retirementyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    mjaccttypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    currmiaccttypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    curracctstatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    mailtypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    mailaddrusecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    openfundsourcecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    owncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    datelastcontact: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datemat: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    taxrptfororgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    taxrptforpersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    branchorgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    nextrtxnnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    closereasoncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    passbookyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    acctdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    addrformatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    rpt1098yn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    rptptsyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    currterm: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    contractdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    transactionacctyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    stmtacctyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    truncateyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    analysisyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    maxoverdraftlimit: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    addrformatdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(40))
    privacyind: Mapped[Optional[str]] = mapped_column(CHAR(1))
    checksyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    checkimageyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    naicsnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The naicsnbr is the user assigned code that identifies the north American industry classification for a person.')
    naicstypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The naics type code is the code used to identify the hierarchical industry group in which each naicscd resides.')
    naicscd: Mapped[Optional[str]] = mapped_column(VARCHAR(6), comment='The government assigned naics industry class code.')
    naicsdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(254), comment='The government assigned naics industry description.')
    siccd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The sic code is the user assigned code that identifies the standard industrial class for a person.')
    sicdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(60), comment='The sic code is the user assigned code that identifies the valid standard industrial class used.')
    sicsubcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The sicsubcd is a user assigned code that identifies the standard industrial class sub that applies to a person. The sicsubcd is a user assigned code that identifies the standard industrial class sub that applies to a person.')
    sicsubdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(60), comment='The sic subordinate description is the textual description of the standard industry class subordinate codes.')
    creditscore: Mapped[Optional[float]] = mapped_column(NUMBER(15, 0, False))
    scoredate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    regeoptin: Mapped[Optional[str]] = mapped_column(VARCHAR(254))
    opendate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    addrnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Address Number is the system assigned number that uniquely identifies each address.')


t_wh_acctaccthold = Table(
    'wh_acctaccthold', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False)),
    Column('holdseqnbr', NUMBER(22, 0, False)),
    Column('rundate', DateTime),
    Column('effdate', DateTime),
    Column('acctholdcd', VARCHAR(4), nullable=False),
    Column('holdamt', NUMBER(22, 3, True)),
    Column('createdatetime', DateTime),
    Column('inactivedate', DateTime),
    Column('loanacctnbr', NUMBER(22, 0, False)),
    Column('acctholddesc', VARCHAR(30)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


class WhAcctcommon(Base):
    __tablename__ = 'wh_acctcommon'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'effdate', name='wh_acctcommon_pk'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    monthendyn: Mapped[str] = mapped_column(CHAR(1), server_default=text("'n' "))
    mjaccttypcd: Mapped[str] = mapped_column(VARCHAR(4))
    currmiaccttypcd: Mapped[str] = mapped_column(VARCHAR(4))
    product: Mapped[str] = mapped_column(VARCHAR(30))
    curracctstatcd: Mapped[str] = mapped_column(VARCHAR(4))
    acctopencurrmonthyn: Mapped[str] = mapped_column(CHAR(1), server_default=text("'n' "))
    acctclosecurrmonthyn: Mapped[str] = mapped_column(CHAR(1), server_default=text("'n' "))
    branchorgnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False))
    bankorgnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('sysdate '))
    curracctstateffdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    branchname: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    noteintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    notenextratechangedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    noteratechangecalpercd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    noteopenamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    notebal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    bookbalance: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='The current PRINCIPAL balance of the account less any amount sold or participated to a third party calculated by summing all NOTE/IBAL and PART/BAL balances.')
    notemtdavgbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    noteintcalcschednbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    calcbaltypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    compoundcalpercd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    daysmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    intmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    intmincalcbaltypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    ratetypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    intbase: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False))
    intminbalamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    datemat: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    currterm: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False))
    contractdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    closedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    taxrptfororgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    taxrptforpersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    origpersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    originatingperson: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    acctofficernbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    acctofficer: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    loanofficersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    loanofficer: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    managingofficernbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    managingofficer: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    nameaddr1: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    nameaddr2: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    nameaddr3: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    nameaddr4: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    nameaddr5: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    ownername: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    ownersortname: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    primaryownerzipcd: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    primaryownerzipcdsuff: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    primaryownercity: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    primaryownerstate: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    homephone: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    businessphone: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    taxidnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(60))


class WhAcctcommonMe(Base):
    __tablename__ = 'wh_acctcommon_me'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'effdate', name='sys_c_snap$_1wh_acctcommon_te'),
        Index('wh_acctcommon_me_dx1', 'acctnbr', 'curracctstatcd', 'mjaccttypcd', 'currmiaccttypcd'),
        Index('wh_acctcommon_me_dx10', 'intmincalcbaltypcd'),
        Index('wh_acctcommon_me_dx11', 'ratetypcd'),
        Index('wh_acctcommon_me_dx12', 'taxrptfororgnbr'),
        Index('wh_acctcommon_me_dx13', 'taxrptforpersnbr'),
        Index('wh_acctcommon_me_dx14', 'origpersnbr'),
        Index('wh_acctcommon_me_dx15', 'acctofficernbr'),
        Index('wh_acctcommon_me_dx16', 'managingofficernbr'),
        Index('wh_acctcommon_me_dx17', 'acctnbr'),
        Index('wh_acctcommon_me_dx2', 'curracctstatcd', 'mjaccttypcd', 'currmiaccttypcd'),
        Index('wh_acctcommon_me_dx3', 'mjaccttypcd', 'currmiaccttypcd'),
        Index('wh_acctcommon_me_dx4', 'branchorgnbr', 'bankorgnbr'),
        Index('wh_acctcommon_me_dx5', 'noteratechangecalpercd'),
        Index('wh_acctcommon_me_dx6', 'calcbaltypcd'),
        Index('wh_acctcommon_me_dx7', 'compoundcalpercd'),
        Index('wh_acctcommon_me_dx8', 'daysmethcd'),
        Index('wh_acctcommon_me_dx9', 'intmethcd'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    monthendyn: Mapped[str] = mapped_column(CHAR(1))
    mjaccttypcd: Mapped[str] = mapped_column(VARCHAR(4))
    currmiaccttypcd: Mapped[str] = mapped_column(VARCHAR(4))
    product: Mapped[str] = mapped_column(VARCHAR(30))
    curracctstatcd: Mapped[str] = mapped_column(VARCHAR(4))
    acctopencurrmonthyn: Mapped[str] = mapped_column(CHAR(1))
    acctclosecurrmonthyn: Mapped[str] = mapped_column(CHAR(1))
    branchorgnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False))
    bankorgnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    curracctstateffdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    branchname: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    noteintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    notenextratechangedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    noteratechangecalpercd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    noteopenamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    notebal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    bookbalance: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    notemtdavgbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    noteintcalcschednbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    calcbaltypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    compoundcalpercd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    daysmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    intmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    intmincalcbaltypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    ratetypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    intbase: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False))
    intminbalamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    datemat: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    currterm: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False))
    contractdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    closedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    taxrptfororgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    taxrptforpersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    origpersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    originatingperson: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    acctofficernbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    acctofficer: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    loanofficersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    loanofficer: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    managingofficernbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    managingofficer: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    nameaddr1: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    nameaddr2: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    nameaddr3: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    nameaddr4: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    nameaddr5: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    ownername: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    ownersortname: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    primaryownerzipcd: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    primaryownerzipcdsuff: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    primaryownercity: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    primaryownerstate: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    homephone: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    businessphone: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    taxidnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(22))


class WhAcctcommonTemp(Base):
    __tablename__ = 'wh_acctcommon_temp'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'effdate', name='wh_acctcommon_temp_pk'),
        Index('wh_acctcommon_temp_dx1', 'acctnbr', 'curracctstatcd', 'mjaccttypcd', 'currmiaccttypcd'),
        Index('wh_acctcommon_temp_dx2', 'curracctstatcd', 'mjaccttypcd', 'currmiaccttypcd'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    monthendyn: Mapped[str] = mapped_column(CHAR(1))
    mjaccttypcd: Mapped[str] = mapped_column(VARCHAR(4))
    currmiaccttypcd: Mapped[str] = mapped_column(VARCHAR(4))
    product: Mapped[str] = mapped_column(VARCHAR(30))
    curracctstatcd: Mapped[str] = mapped_column(VARCHAR(4))
    acctopencurrmonthyn: Mapped[str] = mapped_column(CHAR(1))
    acctclosecurrmonthyn: Mapped[str] = mapped_column(CHAR(1))
    branchorgnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False))
    bankorgnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    curracctstateffdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    branchname: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    noteintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    notenextratechangedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    noteratechangecalpercd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    noteopenamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    notebal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    bookbalance: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='The current PRINCIPAL balance of the account less any amount sold or participated to a third party calculated by summing all NOTE/IBAL and PART/BAL balances.')
    notemtdavgbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    noteintcalcschednbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    calcbaltypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    compoundcalpercd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    daysmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    intmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    intmincalcbaltypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    ratetypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    intbase: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False))
    intminbalamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    datemat: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    currterm: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False))
    contractdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    closedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    taxrptfororgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    taxrptforpersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    origpersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    originatingperson: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    acctofficernbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    acctofficer: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    loanofficersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    loanofficer: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    managingofficernbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    managingofficer: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    nameaddr1: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    nameaddr2: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    nameaddr3: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    nameaddr4: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    nameaddr5: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    ownername: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    ownersortname: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    primaryownerzipcd: Mapped[Optional[str]] = mapped_column(VARCHAR(5))
    primaryownerzipcdsuff: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    primaryownercity: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    primaryownerstate: Mapped[Optional[str]] = mapped_column(VARCHAR(2))
    homephone: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    businessphone: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    taxidnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(22))


class WhAcctdeposit(Base):
    __tablename__ = 'wh_acctdeposit'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'effdate', name='wh_acctdeposit_pk'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('sysdate '))
    transactionacctyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1), server_default=text("'y'"))
    stmtacctyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1), server_default=text("'n'"))
    mmyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1), server_default=text("'n'"))
    passbookyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1), server_default=text("'n'"))
    retirementyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1), server_default=text("'n'"))
    retirementplannbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    sourceoffunds: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    closereasoncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    ytdamtint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdamtpen: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdamtfwth: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdamtswth: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdoverdrafts: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdnsf: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    inerestpmtmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    acctpenmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    mjmipenmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    penfreeamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    noteavail: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    noteaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 6, True))
    overdraftbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    overdraftavail: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    checkholds: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    otherholds: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    stmtcyclecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    sccyclecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    intcyclecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    earningscalperiod: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    nextearningdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datelastcontact: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    odexcessbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcessintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    odexcessaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    odexcessytdint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcesssubacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    limitodbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    limitodintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    limitodaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    limitodytdint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    limitodsubacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    limitodamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))


class WhAcctdepositMe(Base):
    __tablename__ = 'wh_acctdeposit_me'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'effdate', name='sys_c_snap$_4wh_acctdeposit_t'),
        Index('wh_acctdeposit_me_dx1', 'sourceoffunds'),
        Index('wh_acctdeposit_me_dx2', 'closereasoncd'),
        Index('wh_acctdeposit_me_dx3', 'inerestpmtmethcd'),
        Index('wh_acctdeposit_me_dx4', 'acctpenmethcd'),
        Index('wh_acctdeposit_me_dx5', 'mjmipenmethcd'),
        Index('wh_acctdeposit_me_dx6', 'stmtcyclecd'),
        Index('wh_acctdeposit_me_dx7', 'sccyclecd'),
        Index('wh_acctdeposit_me_dx8', 'intcyclecd'),
        Index('wh_acctdeposit_me_dx9', 'acctnbr'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    transactionacctyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    stmtacctyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    mmyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    passbookyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    retirementyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    retirementplannbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    sourceoffunds: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    closereasoncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    ytdamtint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdamtpen: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdamtfwth: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdamtswth: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdoverdrafts: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdnsf: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    inerestpmtmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    acctpenmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    mjmipenmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    penfreeamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    noteavail: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    noteaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 6, True))
    overdraftbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    overdraftavail: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    checkholds: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    otherholds: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    stmtcyclecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    sccyclecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    intcyclecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    earningscalperiod: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    nextearningdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datelastcontact: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    odexcessbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcessintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    odexcessaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    odexcessytdint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcesssubacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    limitodbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    limitodintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    limitodaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    limitodytdint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    limitodsubacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    limitodamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))


class WhAcctdepositTemp(Base):
    __tablename__ = 'wh_acctdeposit_temp'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'effdate', name='wh_acctdeposit_temp_pk'),
        Index('wh_acctdeposit_temp_dx1', 'acctnbr'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    transactionacctyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    stmtacctyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    mmyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    passbookyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    retirementyn: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    retirementplannbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    sourceoffunds: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    closereasoncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    ytdamtint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdamtpen: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdamtfwth: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdamtswth: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdoverdrafts: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdnsf: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    inerestpmtmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    acctpenmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    mjmipenmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    penfreeamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    noteavail: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    noteaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 6, True))
    overdraftbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    overdraftavail: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    checkholds: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    otherholds: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    stmtcyclecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    sccyclecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    intcyclecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    earningscalperiod: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    nextearningdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datelastcontact: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    odexcessbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcessintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    odexcessaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    odexcessytdint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcesssubacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    limitodbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    limitodintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    limitodaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    limitodytdint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    limitodsubacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    limitodamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))


class WhAcctloan(Base):
    __tablename__ = 'wh_acctloan'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'effdate', name='wh_acctloan_pk'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    pmtmethcd: Mapped[str] = mapped_column(VARCHAR(4))
    gracedays: Mapped[float] = mapped_column(NUMBER(8, 0, False))
    demandyn: Mapped[str] = mapped_column(CHAR(1), server_default=text("'n' "))
    restructuredyn: Mapped[str] = mapped_column(CHAR(1), server_default=text("'n' "))
    notreyn: Mapped[str] = mapped_column(CHAR(1), server_default=text("'n' "))
    balloonyn: Mapped[str] = mapped_column(CHAR(1), server_default=text("'n' "))
    invrconformyn: Mapped[str] = mapped_column(CHAR(1), server_default=text("'n' "))
    billadvanceyn: Mapped[str] = mapped_column(CHAR(1), server_default=text("'n' "))
    ratechangerecalcpmtyn: Mapped[str] = mapped_column(CHAR(1), server_default=text("'n' "))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('sysdate '))
    invrnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    propnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    escbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    unappbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    lipbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    cobal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    latechargedue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    noteaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    notenonaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    escaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    escintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    purpcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    lnqualitycd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    fdiccatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    fhlbcatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    occloancatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    otsloancatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    date1stpmtdue: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    nextduedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    nextpmtchangedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    creditreporttypcd: Mapped[Optional[str]] = mapped_column(CHAR(4))
    esccompmth: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    loansourcecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    loanlosscatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    totalpctsold: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(24, 10, True))
    riskratingcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    loanagencycd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    currduedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    slpcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    cracatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    lastreviewdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    lastpaymentdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    marginfixed: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 8, True))
    marginpct: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    maxratechangeup: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    minratechangeup: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    minintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    maxintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    capitalizeintyn: Mapped[Optional[str]] = mapped_column(CHAR(1), server_default=text("'n'"))
    amortterm: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False))
    ratechangerndmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    pmtchangerndmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    minratechangedown: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    maxratechangedown: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    negamortallowedyn: Mapped[Optional[str]] = mapped_column(CHAR(1), server_default=text("'n'"))
    adjusttermyn: Mapped[Optional[str]] = mapped_column(CHAR(1), server_default=text("'n'"))
    pmtchangecalpercd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    creditlimitamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    origintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    origloanlimit: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    prepaycharge: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    totalpi: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    totalpidue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    escrowdue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    totalpaymentsdue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    numberpmtsdue: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False))
    ytdlate30: Mapped[Optional[float]] = mapped_column(NUMBER(4, 0, False))
    ytdlate60: Mapped[Optional[float]] = mapped_column(NUMBER(4, 0, False))
    ytdlate90: Mapped[Optional[float]] = mapped_column(NUMBER(4, 0, False))
    ytdlate120plus: Mapped[Optional[float]] = mapped_column(NUMBER(4, 0, False))
    ytdinterest: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdlatechrgpaid: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdprepaidcharge: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    defcostrem: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    defcostunearned: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    defcostrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(20, 7, True))
    defcostratemonthly: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(20, 7, True))
    stndcostrem: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    stndcostunearned: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    stndcostrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    stndcostratemonthly: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    deffeerem: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    deffeeunearned: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    deffeerate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(20, 7, True))
    deffeeratemonthly: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(20, 7, True))
    defremterm: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    mlacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    calldate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    estdatemat: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    intpdtoprinbalance: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    privatebalance: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    shadowacctgyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    shadowacctgstartdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    shadowacctgenddate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    transferservorgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    transferserveffdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    transferservdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    transferservpurchasedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    intfirstconvertdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    schedulebal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    refiprioracctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    ytdaccrued: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True))
    limitodbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    limitodintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    limitodaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    limitodytdintchrg: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    limitodbalsubacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    limitodamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcessbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcessintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    odexcessaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    odexcessytdint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcesssubacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    aragingeffdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    aragingcatsumamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    credlimitclatresamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    credlimitclatreseffdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    sbaacctnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    sbadisbursementdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    pppdeffprincipalamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    pppdeffinterestamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))


class WhAcctloanMe(Base):
    __tablename__ = 'wh_acctloan_me'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'effdate', name='sys_c_snap$_1221wh_acctloan_temp_pk'),
        Index('wh_acctloan_me_dx1', 'acctnbr'),
        Index('wh_acctloan_me_dx10', 'esccompmth'),
        Index('wh_acctloan_me_dx11', 'loansourcecd'),
        Index('wh_acctloan_me_dx12', 'loanlosscatcd'),
        Index('wh_acctloan_me_dx13', 'riskratingcd'),
        Index('wh_acctloan_me_dx14', 'loanagencycd'),
        Index('wh_acctloan_me_dx15', 'slpcd'),
        Index('wh_acctloan_me_dx16', 'cracatcd'),
        Index('wh_acctloan_me_dx2', 'purpcd'),
        Index('wh_acctloan_me_dx3', 'lnqualitycd'),
        Index('wh_acctloan_me_dx4', 'fdiccatcd'),
        Index('wh_acctloan_me_dx5', 'fhlbcatcd'),
        Index('wh_acctloan_me_dx6', 'pmtmethcd'),
        Index('wh_acctloan_me_dx7', 'occloancatcd'),
        Index('wh_acctloan_me_dx8', 'otsloancatcd'),
        Index('wh_acctloan_me_dx9', 'creditreporttypcd'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    pmtmethcd: Mapped[str] = mapped_column(VARCHAR(4))
    gracedays: Mapped[float] = mapped_column(NUMBER(8, 0, False))
    demandyn: Mapped[str] = mapped_column(CHAR(1))
    restructuredyn: Mapped[str] = mapped_column(CHAR(1))
    notreyn: Mapped[str] = mapped_column(CHAR(1))
    balloonyn: Mapped[str] = mapped_column(CHAR(1))
    invrconformyn: Mapped[str] = mapped_column(CHAR(1))
    billadvanceyn: Mapped[str] = mapped_column(CHAR(1))
    ratechangerecalcpmtyn: Mapped[str] = mapped_column(CHAR(1))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    invrnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    propnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    escbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    unappbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    lipbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    cobal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    latechargedue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    noteaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    notenonaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    escaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    escintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    purpcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    lnqualitycd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    fdiccatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    fhlbcatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    occloancatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    otsloancatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    date1stpmtdue: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    nextduedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    nextpmtchangedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    creditreporttypcd: Mapped[Optional[str]] = mapped_column(CHAR(4))
    esccompmth: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    loansourcecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    loanlosscatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    totalpctsold: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(24, 10, True))
    riskratingcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    loanagencycd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    currduedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    slpcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    cracatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    lastreviewdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    lastpaymentdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    marginfixed: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 8, True))
    marginpct: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    maxratechangeup: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    minratechangeup: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    minintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    maxintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    capitalizeintyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    amortterm: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False))
    ratechangerndmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    pmtchangerndmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    minratechangedown: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    maxratechangedown: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    negamortallowedyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    adjusttermyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    pmtchangecalpercd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    creditlimitamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    origintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    origloanlimit: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    prepaycharge: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    totalpi: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    totalpidue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    escrowdue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    totalpaymentsdue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    numberpmtsdue: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False))
    ytdlate30: Mapped[Optional[float]] = mapped_column(NUMBER(4, 0, False))
    ytdlate60: Mapped[Optional[float]] = mapped_column(NUMBER(4, 0, False))
    ytdlate90: Mapped[Optional[float]] = mapped_column(NUMBER(4, 0, False))
    ytdlate120plus: Mapped[Optional[float]] = mapped_column(NUMBER(4, 0, False))
    ytdinterest: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdlatechrgpaid: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdprepaidcharge: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    defcostrem: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    defcostunearned: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    defcostrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(20, 7, True))
    defcostratemonthly: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(20, 7, True))
    stndcostrem: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    stndcostunearned: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    stndcostrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    stndcostratemonthly: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    deffeerem: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    deffeeunearned: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    deffeerate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(20, 7, True))
    deffeeratemonthly: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(20, 7, True))
    defremterm: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    mlacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    calldate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    estdatemat: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    intpdtoprinbalance: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    privatebalance: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    shadowacctgyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    shadowacctgstartdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    shadowacctgenddate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    transferservorgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    transferserveffdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    transferservdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    transferservpurchasedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    intfirstconvertdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    schedulebal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    refiprioracctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    ytdaccrued: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True))
    limitodbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    limitodintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    limitodaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    limitodytdintchrg: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    limitodbalsubacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    limitodamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcessbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcessintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    odexcessaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    odexcessytdint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcesssubacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    aragingeffdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    aragingcatsumamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    credlimitclatresamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    credlimitclatreseffdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    sbaacctnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    sbadisbursementdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    pppdeffprincipalamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    pppdeffinterestamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))


class WhAcctloanTemp(Base):
    __tablename__ = 'wh_acctloan_temp'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'effdate', name='wh_acctloan_temp_pk'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    pmtmethcd: Mapped[str] = mapped_column(VARCHAR(4))
    gracedays: Mapped[float] = mapped_column(NUMBER(8, 0, False))
    demandyn: Mapped[str] = mapped_column(CHAR(1))
    restructuredyn: Mapped[str] = mapped_column(CHAR(1))
    notreyn: Mapped[str] = mapped_column(CHAR(1))
    balloonyn: Mapped[str] = mapped_column(CHAR(1))
    invrconformyn: Mapped[str] = mapped_column(CHAR(1))
    billadvanceyn: Mapped[str] = mapped_column(CHAR(1))
    ratechangerecalcpmtyn: Mapped[str] = mapped_column(CHAR(1))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    invrnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    propnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    escbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    unappbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    lipbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    cobal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    latechargedue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    noteaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    notenonaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    escaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    escintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    purpcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    lnqualitycd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    fdiccatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    fhlbcatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    occloancatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    otsloancatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    date1stpmtdue: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    nextduedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    nextpmtchangedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    creditreporttypcd: Mapped[Optional[str]] = mapped_column(CHAR(4))
    esccompmth: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    loansourcecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    loanlosscatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    totalpctsold: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(24, 10, True))
    riskratingcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    loanagencycd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    currduedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    slpcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    cracatcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    lastreviewdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    lastpaymentdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    marginfixed: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 8, True))
    marginpct: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    maxratechangeup: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    minratechangeup: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    minintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    maxintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    capitalizeintyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    amortterm: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False))
    ratechangerndmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    pmtchangerndmethcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    minratechangedown: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    maxratechangedown: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    negamortallowedyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    adjusttermyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    pmtchangecalpercd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    creditlimitamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    origintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    origloanlimit: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    prepaycharge: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    totalpi: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    totalpidue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    escrowdue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    totalpaymentsdue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    numberpmtsdue: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False))
    ytdlate30: Mapped[Optional[float]] = mapped_column(NUMBER(4, 0, False))
    ytdlate60: Mapped[Optional[float]] = mapped_column(NUMBER(4, 0, False))
    ytdlate90: Mapped[Optional[float]] = mapped_column(NUMBER(4, 0, False))
    ytdlate120plus: Mapped[Optional[float]] = mapped_column(NUMBER(4, 0, False))
    ytdinterest: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdlatechrgpaid: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    ytdprepaidcharge: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    defcostrem: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    defcostunearned: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    defcostrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(20, 7, True))
    defcostratemonthly: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(20, 7, True))
    stndcostrem: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    stndcostunearned: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    stndcostrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    stndcostratemonthly: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    deffeerem: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    deffeeunearned: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    deffeerate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(20, 7, True))
    deffeeratemonthly: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(20, 7, True))
    defremterm: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    mlacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    calldate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    estdatemat: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    intpdtoprinbalance: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    privatebalance: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    shadowacctgyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    shadowacctgstartdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    shadowacctgenddate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    transferservorgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    transferserveffdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    transferservdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    transferservpurchasedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    intfirstconvertdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    schedulebal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    refiprioracctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    ytdaccrued: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True))
    limitodbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    limitodintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    limitodaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    limitodytdintchrg: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    limitodbalsubacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    limitodamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcessbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcessintrate: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(8, 7, True))
    odexcessaccruedint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    odexcessytdint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    odexcesssubacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    aragingeffdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    aragingcatsumamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    credlimitclatresamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))
    credlimitclatreseffdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    sbaacctnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(64))
    sbadisbursementdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    pppdeffprincipalamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))
    pppdeffinterestamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True))


t_wh_acctlockout = Table(
    'wh_acctlockout', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False),
    Column('effdate', DateTime, nullable=False),
    Column('lockoutflagdesc', VARCHAR(30)),
    Column('rundate', DateTime, nullable=False),
    Column('lockoutflagcd', VARCHAR(4), nullable=False),
    Column('inactivedate', DateTime),
    Column('notenbr', NUMBER(22, 0, False)),
    Column('notificationyn', CHAR(1), nullable=False),
    Column('notifyonlyontxnyn', CHAR(1), nullable=False),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_acctrole = Table(
    'wh_acctrole', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('acctrolecd', VARCHAR(4), nullable=False),
    Column('persnbr', NUMBER(22, 0, False)),
    Column('acctroledesc', VARCHAR(30)),
    Column('org_orgnbr', NUMBER(22, 0, False)),
    Column('datelastmaint', DateTime, nullable=False),
    Index('wh_acctrole_dx1', 'acctnbr'),
    schema='COCCDM'
)


t_wh_acctuserfields = Table(
    'wh_acctuserfields', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False, comment='The Account Number is a system-assigned primary key that uniquely identifies each account. '),
    Column('acctuserfieldcd', VARCHAR(4), comment='The Account User Field Code is the user field code associated with the account. '),
    Column('acctuserfieldcddesc', VARCHAR(100), comment='The Account User Field Code Description is the description of the user field code.'),
    Column('acctuserfieldvalue', VARCHAR(254)),
    Column('acctuserfieldvaluedesc', VARCHAR(254)),
    Column('acctdatelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when this ACCTUSERFIELDS row was most recently updated. SYSTEM  USE  ONLY'),
    Column('rundate', DateTime, comment='The post date when this WH_ACCTUSERFIELD Table was populated. SYSTEM  USE  ONLY'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when this WH_ACCTUSERFIELD Table was populated. SYSTEM  USE  ONLY'),
    schema='COCCDM'
)


t_wh_addr = Table(
    'wh_addr', Base.metadata,
    Column('addrnbr', NUMBER(22, 0, False), nullable=False),
    Column('linenbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('ctrycd', VARCHAR(4), nullable=False),
    Column('nextlinenbr', NUMBER(22, 0, False)),
    Column('ctrysubdivcd', VARCHAR(4)),
    Column('ctrymailcd', VARCHAR(9)),
    Column('statecd', VARCHAR(4)),
    Column('cityname', VARCHAR(30)),
    Column('citynamesndx', VARCHAR(4)),
    Column('zipcd', VARCHAR(5)),
    Column('zipsuf', VARCHAR(4)),
    Column('censustrtnbr', VARCHAR(6)),
    Column('smsanbr', VARCHAR(5)),
    Column('postnetcd', VARCHAR(2)),
    Column('addrlinetypcd1', VARCHAR(4)),
    Column('text1', VARCHAR(40)),
    Column('addrlinetypdesc1', VARCHAR(30)),
    Column('addrlinetypseq1', NUMBER(22, 0, False)),
    Column('addrtextsndx1', VARCHAR(4)),
    Column('addrlinetypcd2', VARCHAR(4)),
    Column('text2', VARCHAR(40)),
    Column('addrlinetypdesc2', VARCHAR(30)),
    Column('addrlinetypseq2', NUMBER(22, 0, False)),
    Column('addrtextsndx2', VARCHAR(4)),
    Column('addrlinetypcd3', VARCHAR(4)),
    Column('text3', VARCHAR(40)),
    Column('addrlinetypdesc3', VARCHAR(30)),
    Column('addrlinetypseq3', NUMBER(22, 0, False)),
    Column('addrtextsndx3', VARCHAR(4)),
    Column('addrlinetypcd4', VARCHAR(4)),
    Column('text4', VARCHAR(40)),
    Column('addrlinetypdesc4', VARCHAR(30)),
    Column('addrlinetypseq4', NUMBER(22, 0, False)),
    Column('addrtextsndx4', VARCHAR(4)),
    Column('addrlinetypcd5', VARCHAR(4)),
    Column('text5', VARCHAR(40)),
    Column('addrlinetypdesc5', VARCHAR(30)),
    Column('addrlinetypseq5', NUMBER(22, 0, False)),
    Column('addrtextsndx5', VARCHAR(4)),
    Column('addrlinetypcd6', VARCHAR(4)),
    Column('text6', VARCHAR(40)),
    Column('addrlinetypdesc6', VARCHAR(30)),
    Column('addrlinetypseq6', NUMBER(22, 0, False)),
    Column('addrtextsndx6', VARCHAR(4)),
    Column('addrlinetypcd7', VARCHAR(4)),
    Column('text7', VARCHAR(40)),
    Column('addrlinetypdesc7', VARCHAR(30)),
    Column('addrlinetypseq7', NUMBER(22, 0, False)),
    Column('addrtextsndx7', VARCHAR(4)),
    Column('mailaddryn', CHAR(1), nullable=False),
    Column('mailtypcd', VARCHAR(4)),
    Column('mailtypdesc', VARCHAR(30)),
    Column('addrusecd', VARCHAR(4)),
    Column('addrusedesc', VARCHAR(30)),
    Column('electronicyn', CHAR(1)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_agreement = Table(
    'wh_agreement', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False),
    Column('agreenbr', NUMBER(22, 0, False), nullable=False),
    Column('persnbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('effdate', DateTime),
    Column('inactivedate', DateTime),
    Column('cyclewthdllimitamt', NUMBER(22, 2, True)),
    Column('cycledepositlimitamt', NUMBER(22, 2, True)),
    Column('prefix', NUMBER(22, 0, False)),
    Column('cardnbr', NUMBER(22, 0, False)),
    Column('agreetypcd', VARCHAR(4), nullable=False),
    Column('ownerpersnbr', NUMBER(22, 0, False)),
    Column('ownerorgnbr', NUMBER(22, 0, False)),
    Column('nextmembernbr', NUMBER(22, 0, False)),
    Column('servchgacctnbr', NUMBER(22, 0, False)),
    Column('nextservchgdate', DateTime),
    Column('servchgwaiveyn', CHAR(1), nullable=False),
    Column('maintchgwaiveyn', CHAR(1), nullable=False),
    Column('extcardnbr', VARCHAR(32)),
    Column('datelastmaint', DateTime, nullable=False),
    Index('wh_agreement_dx1', 'acctnbr', 'agreetypcd', 'inactivedate'),
    Index('wh_agreement_dx2', 'acctnbr', 'agreetypcd', 'agreenbr', 'prefix'),
    schema='COCCDM'
)


t_wh_allroles = Table(
    'wh_allroles', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False, comment='The Account Number is a system-assigned primary key that uniquely identifies each account. '),
    Column('acctrolecd', VARCHAR(20), comment='The Account Role Code is a user defined code used to identify account roles. '),
    Column('acctroledesc', VARCHAR(30), comment='The Account Role Description is the textual description of the role codes used.'),
    Column('emplroleyn', VARCHAR(1), comment='EmployRoleYN identifies if the role is for internal bank employee processing. '),
    Column('persnbr', NUMBER(22, 0, False), comment='The Person number for the account role'),
    Column('orgnbr', NUMBER(22, 0, False), comment='The organization number for the account role.'),
    Column('rundate', DateTime, comment='The Bank Post date . '),
    Column('datelastmaint', DateTime, nullable=False, comment='The date when this row was most recently updated. SYSTEM  USE  ONLY'),
    schema='COCCDM'
)


t_wh_appraisal = Table(
    'wh_appraisal', Base.metadata,
    Column('propnbr', NUMBER(22, 0, False), nullable=False),
    Column('effdate', DateTime, nullable=False),
    Column('aprstypcd', VARCHAR(4), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('aprsvalueamt', NUMBER(22, 0, False)),
    Column('aprstypdesc', VARCHAR(30)),
    Column('datelastmaint', DateTime, nullable=False),
    Column('aprsorgnbr', NUMBER(22, 0, False)),
    schema='COCCDM'
)


t_wh_cards = Table(
    'wh_cards', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False),
    Column('agreenbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('agreetypcd', VARCHAR(4)),
    Column('cardnbr', NUMBER(22, 0, False)),
    Column('currstatuscd', VARCHAR(4)),
    Column('issuedate', DateTime),
    Column('expiredate', DateTime),
    Column('datelasttran', DateTime),
    Column('persnbr', NUMBER(22, 0, False)),
    Column('membernbr', NUMBER(22, 0, False)),
    Column('datelastmaint', DateTime, nullable=False),
    Index('wh_cards_dx1', 'acctnbr', 'agreenbr', unique=True),
    schema='COCCDM'
)


t_wh_cards2 = Table(
    'wh_cards2', Base.metadata,
    Column('agreenbr', NUMBER(22, 0, False)),
    Column('primarychecking', NUMBER(22, 0, False)),
    Column('primarysavings', NUMBER(22, 0, False)),
    Column('rundate', DateTime, nullable=False),
    Column('membernbr', NUMBER(22, 0, False)),
    Column('persnbr', NUMBER(22, 0, False)),
    Column('currissuenbr', NUMBER(22, 0, False)),
    Column('pinoffset', VARCHAR(8)),
    Column('datelasttran', DateTime),
    Column('issuenbr', NUMBER(22, 0, False)),
    Column('issuedate', DateTime),
    Column('expiredate', DateTime),
    Column('currstatuscd', VARCHAR(4)),
    Column('pintrylimit', NUMBER(22, 0, False)),
    Column('atmwthdllimitamt', NUMBER(22, 0, False)),
    Column('poswthdllimitamt', NUMBER(22, 0, False)),
    Column('atmdebitlimitamt', NUMBER(22, 0, False)),
    Column('poscreditlimitamt', NUMBER(22, 0, False)),
    Column('usesperdaylimit', NUMBER(22, 0, False)),
    Column('depositlimitamt', NUMBER(22, 0, False)),
    Column('cashbacklimitamt', NUMBER(22, 0, False)),
    Column('calcyclecd', VARCHAR(4)),
    Column('combineddailywthdllimitamt', NUMBER(22, 0, False)),
    Column('currmembernbr', NUMBER(22, 0, False)),
    Column('userid', VARCHAR(16)),
    Column('datelastmaint', DateTime, nullable=False),
    Index('wh_cards2_dx1', 'agreenbr', 'primarychecking'),
    schema='COCCDM'
)


t_wh_cashboxrtxn = Table(
    'wh_cashboxrtxn', Base.metadata,
    Column('cashboxnbr', NUMBER(22, 0, False), nullable=False, comment='The Cash Box Number identifies cash box related to the transaction.'),
    Column('cashboxtxnnbr', NUMBER(22, 0, False), nullable=False, comment='The Cash Box Transaction Number is a system assigned number that uniquely identifies each transaction.'),
    Column('cashboxtypcd', VARCHAR(4), comment='The Cash Box Type Code is the code that identifies the type of cash boxes.'),
    Column('cashboxtypdesc', VARCHAR(30), comment='The Cash Box Type Description provides a textual description of the cash box types.'),
    Column('cashboxtxntypcd', VARCHAR(4), comment='The Cash Box Transaction Type Code is the code that identifies the type of transaction for the cash box.'),
    Column('cashboxtxntypdesc', VARCHAR(30), comment='The Cash Box Transaction Type is the textual description of the different transaction types.'),
    Column('branchorgnbr', NUMBER(22, 0, False), comment='The Location Organization Number is assigned to identify the location of the cash box.'),
    Column('parentcashboxnbr', NUMBER(22, 0, False), comment='The Parent Cash Box identifies the cashbox that was the parent for the transaction.'),
    Column('parentcashboxtxnnbr', NUMBER(22, 0, False), comment='The Parent Cash Box is the transaction number of the Parent Cash Box.'),
    Column('origpersnbr', NUMBER(22, 0, False), comment='The Original Person Number is the person who performed the transaction.'),
    Column('apprpersnbr', NUMBER(22, 0, False), comment='The Approval Person is the number of the person who gave approval for this transaction.'),
    Column('otcpersnbr', NUMBER(22, 0, False), comment='The OTC Person is the number of the over the counter person.'),
    Column('cashboxtxndesc', VARCHAR(60), comment='The Cash Box Transaction Description is the textual description for a cashbox transaction.'),
    Column('currrtxnstatcd', VARCHAR(4), nullable=False, server_default=text("'C' "), comment='The Current Transaction code identifies the current status.'),
    Column('amt', NUMBER(22, 3, True), comment='The amount of the transaction.'),
    Column('holdacctnbr', NUMBER(22, 0, False), comment='The Hold Account Number is the account number for the hold.'),
    Column('effdate', DateTime, comment='The Effective Date of the transaction.'),
    Column('postdate', DateTime, comment='The Posting Date of the transaction.'),
    Column('actdatetime', DateTime, comment='The Active Date Time the cash box was active.'),
    Column('rundate', DateTime, comment='The date that the report was run.'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM  USE  ONLY'),
    schema='COCCDM'
)


t_wh_cashboxrtxn_temp = Table(
    'wh_cashboxrtxn_temp', Base.metadata,
    Column('cashboxnbr', NUMBER(22, 0, False), nullable=False, comment='The Cash Box Number identifies cash box related to the transaction.'),
    Column('cashboxtxnnbr', NUMBER(22, 0, False), nullable=False, comment='The Cash Box Transaction Number is a system assigned number that uniquely identifies each transaction.'),
    Column('cashboxtypcd', VARCHAR(4), comment='The Cash Box Type Code is the code that identifies the type of cash boxes.'),
    Column('cashboxtypdesc', VARCHAR(30), comment='The Cash Box Type Description provides a textual description of the cash box types.'),
    Column('cashboxtxntypcd', VARCHAR(4), comment='The Cash Box Transaction Type Code is the code that identifies the type of transaction for the cash box.'),
    Column('cashboxtxntypdesc', VARCHAR(30), comment='The Cash Box Transaction Type is the textual description of the different transaction types.'),
    Column('branchorgnbr', NUMBER(22, 0, False), comment='The Location Organization Number is assigned to identify the location of the cash box.'),
    Column('parentcashboxnbr', NUMBER(22, 0, False), comment='The Parent Cash Box identifies the cashbox that was the parent for the transaction.'),
    Column('parentcashboxtxnnbr', NUMBER(22, 0, False), comment='The Parent Cash Box is the transaction number of the Parent Cash Box.'),
    Column('origpersnbr', NUMBER(22, 0, False), comment='The Original Person Number is the person who performed the transaction.'),
    Column('apprpersnbr', NUMBER(22, 0, False), comment='The Approval Person is the number of the person who gave approval for this transaction.'),
    Column('otcpersnbr', NUMBER(22, 0, False), comment='The OTC Person is the number of the over the counter person.'),
    Column('cashboxtxndesc', VARCHAR(60), comment='The Cash Box Transaction Description is the textual description for a cashbox transaction.'),
    Column('currrtxnstatcd', VARCHAR(4), nullable=False, server_default=text("'C' "), comment='The Current Transaction code identifies the current status.'),
    Column('amt', NUMBER(22, 3, True), comment='The amount of the transaction.'),
    Column('holdacctnbr', NUMBER(22, 0, False), comment='The Hold Account Number is the account number for the hold.'),
    Column('effdate', DateTime, comment='The Effective Date of the transaction.'),
    Column('postdate', DateTime, comment='The Posting Date of the transaction.'),
    Column('actdatetime', DateTime, comment='The Active Date Time the cash box was active.'),
    Column('rundate', DateTime, comment='The date that the report was run.'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM  USE  ONLY'),
    schema='COCCDM'
)


t_wh_cashboxrtxnfundtyp = Table(
    'wh_cashboxrtxnfundtyp', Base.metadata,
    Column('cashboxnbr', NUMBER(22, 0, False), nullable=False, comment='The Cash Box Number is a system assigned number used to identify each cash box.'),
    Column('cashboxtxnnbr', NUMBER(22, 0, False), nullable=False, comment='The Cash Box Transaction Number is the system assigned transaction number.'),
    Column('fundtypcd', VARCHAR(4), nullable=False, comment='The Fund Type Code is the code used to identify the funds used in the transaction.'),
    Column('fundtypdesc', VARCHAR(30), comment='The Fund Type Description is the textual description of the fund type.'),
    Column('fundtypdtlcd', VARCHAR(4), nullable=False, comment='The Fund Type Detail Code is the code used to identify the detail for a transaction.'),
    Column('fundtypdtldesc', VARCHAR(30), comment='The Fund Type Detail Description is the textual description of the fund types detail.'),
    Column('clearcatcd', VARCHAR(4), nullable=False, comment='The Clear Category Code is the code used to identify the clear category or check holds on a transaction.'),
    Column('clearcatdesc', VARCHAR(30), comment='The Clearing Category Description is the textual description of the different clearing categories.'),
    Column('amt', NUMBER(22, 3, True), comment='The Amount is the transaction dollar amount.'),
    Column('seqnbr', NUMBER(22, 0, False), comment='The Sequence Number is the system assigned number that identifies the sequence in a transaction.'),
    Column('nbrofitems', NUMBER(22, 0, False), comment='The Number Of Items is the number of checks in a transaction.'),
    Column('datelastmaint', DateTime, comment='The date when this row was most recently updated. SYSTEM  USE  ONLY'),
    Column('rundate', DateTime, server_default=text('SYSDATE'), comment='The date when the batch queue was run.'),
    Column('actdatetime', DateTime, comment='The Active Date Time the cash box was active.'),
    schema='COCCDM'
)


t_wh_cashboxrtxnfundtyp_temp = Table(
    'wh_cashboxrtxnfundtyp_temp', Base.metadata,
    Column('cashboxnbr', NUMBER(22, 0, False), nullable=False, comment='The Cash Box Number is a system assigned number used to identify each cash box.'),
    Column('cashboxtxnnbr', NUMBER(22, 0, False), nullable=False, comment='The Cash Box Transaction Number is the system assigned transaction number.'),
    Column('fundtypcd', VARCHAR(4), nullable=False, comment='The Fund Type Code is the code used to identify the funds used in the transaction.'),
    Column('fundtypdesc', VARCHAR(30), comment='The Fund Type Description is the textual description of the fund type.'),
    Column('fundtypdtlcd', VARCHAR(4), nullable=False, comment='The Fund Type Detail Code is the code used to identify the detail for a transaction.'),
    Column('fundtypdtldesc', VARCHAR(30), comment='The Fund Type Detail Description is the textual description of the fund types detail.'),
    Column('clearcatcd', VARCHAR(4), nullable=False, comment='The Clear Category Code is the code used to identify the clear category or check holds on a transaction.'),
    Column('clearcatdesc', VARCHAR(30), comment='The Clearing Category Description is the textual description of the different clearing categories.'),
    Column('amt', NUMBER(22, 3, True), comment='The Amount is the transaction dollar amount.'),
    Column('seqnbr', NUMBER(22, 0, False), comment='The Sequence Number is the system assigned number that identifies the sequence in a transaction.'),
    Column('nbrofitems', NUMBER(22, 0, False), comment='The Number Of Items is the number of checks in a transaction.'),
    Column('datelastmaint', DateTime, comment='The date when this row was most recently updated. SYSTEM  USE  ONLY'),
    Column('rundate', DateTime, server_default=text('SYSDATE'), comment='The date when the batch queue was run.'),
    Column('actdatetime', DateTime, comment='The Active Date Time the cash box was active.'),
    schema='COCCDM'
)


class WhCheckfree(Base):
    __tablename__ = 'wh_checkfree'
    __table_args__ = (
        PrimaryKeyConstraint('filenumber', 'recordnumber', name='pk_wh_checkfree'),
        {'schema': 'COCCDM'}
    )

    filenumber: Mapped[float] = mapped_column(NUMBER(asdecimal=False), primary_key=True, comment='The payment file received from CheckFree is assigned a number by IB_CheckFreeUpload.')
    recordnumber: Mapped[float] = mapped_column(NUMBER(asdecimal=False), primary_key=True, comment='Represents a row on OSIEXTN.CheckFreeFileRecord.')
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, comment='The run date of the extract.')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='The date the table row was most recently updated.')
    cspid: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment='A unique identifier for the payee, assigned by the CSP.')
    subscriberid: Mapped[Optional[str]] = mapped_column(VARCHAR(55), comment='A unique identifier for the subscriber (assigned by CheckFree).')
    debitacctno: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Account number for the debit account.')
    subscriberfirstname: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment="The subscriber's first name.")
    subscriberlastname: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment="The subscriber's last name.")
    subscribermiddlename: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment="The subscriber's middle name.")
    subscriberaddress1: Mapped[Optional[str]] = mapped_column(VARCHAR(40), comment="First line of the subscriber's mailing address.")
    subscriberaddress2: Mapped[Optional[str]] = mapped_column(VARCHAR(40), comment='Additional mailing address information for the subscriber.')
    subscribercity: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment="The city for the subscriber's address.")
    subscriberstate: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment="The state for the subscriber's address.")
    subscriberzipcd: Mapped[Optional[str]] = mapped_column(VARCHAR(5), comment="The five-digit zip code for the subscriber's address.")
    subscriberzipplus4: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment="The four-digit zip code for the subscriber's address.")
    subscriberzipplus2: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment="The two-digit zip code for the subscriber's address.")
    filetrackid: Mapped[Optional[str]] = mapped_column(VARCHAR(10), comment='Identifies the file from which the payment originated.')
    paymentdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The date the payment should be made based on the request.')
    paymentamount: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='The amount of the payment.')
    paymenttypedescr: Mapped[Optional[str]] = mapped_column(VARCHAR(40), comment='Valid values:P Paper D Draft E Electronic I Internal')
    paymentmatchtypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(3), comment='The method CheckFree uses to match a payment to a standard or managed payee.')
    paymentmatchtypdescr: Mapped[Optional[str]] = mapped_column(VARCHAR(100), comment='The description of payment match type code.')
    standardpayeename: Mapped[Optional[str]] = mapped_column(VARCHAR(35), comment='The payee name assigned to this payment by the subscriber.')
    payeeaddress1: Mapped[Optional[str]] = mapped_column(VARCHAR(40), comment='Mailing address of payee.')
    payeeaddress2: Mapped[Optional[str]] = mapped_column(VARCHAR(40), comment='Additional mailing address information for the payee.')
    payeecity: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment="The city for the payee's address.")
    payeestate: Mapped[Optional[str]] = mapped_column(VARCHAR(2), comment="The state for the payee's address.")
    payeezipcd: Mapped[Optional[str]] = mapped_column(VARCHAR(5), comment="The five-digit zip code for the payee's address.")
    payeezipplus4: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment="The four-digit zip code extension for the payee's address.")
    payeezipplus2: Mapped[Optional[str]] = mapped_column(VARCHAR(2), comment="The two-digit zip code extension for the payee's address.")
    paymentmethodcd: Mapped[Optional[str]] = mapped_column(VARCHAR(2), comment='The method used to issue the payment.')
    paymentmethoddescr: Mapped[Optional[str]] = mapped_column(VARCHAR(100), comment='The description of the payment method.')
    paymenttransactioncd: Mapped[Optional[str]] = mapped_column(VARCHAR(2), comment='The type of transaction.')
    paymenttransactiondescr: Mapped[Optional[str]] = mapped_column(VARCHAR(100), comment='The description of payment transaction.')
    recurringpaymenttypeind: Mapped[Optional[str]] = mapped_column(VARCHAR(1), comment='Indicates if the payment is a single or recurring payment.')
    ebillautopayindicator: Mapped[Optional[str]] = mapped_column(VARCHAR(1), comment='Indicates if the payment originated from an e-bill automatic payment.Valid values:E E-bill Auto-Pay <space> Payment did not originate from an e-bill Auto-Pay')
    ebillindicator: Mapped[Optional[str]] = mapped_column(VARCHAR(1), comment='Indicates whether the payment is associated with an electronic bill. Valid values: Y Payment is associated with an e-bill N Payment is not associated with an e-bill')
    paymentcategory: Mapped[Optional[str]] = mapped_column(VARCHAR(40), comment="The description of payment's category.")
    checknumber: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False), comment='The sequential check number if the payment is processed as a paper check.')
    persnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The system assigned number that identifies every person in Insight.')
    orgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The system assigned number that identifies every organization in Insight.')
    filecreationdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='Date the file was originally created.')


class WhCheckfreeTemp(Base):
    __tablename__ = 'wh_checkfree_temp'
    __table_args__ = (
        PrimaryKeyConstraint('filenumber', 'recordnumber', name='pk_wh_checkfree_temp'),
        {'schema': 'COCCDM'}
    )

    filenumber: Mapped[float] = mapped_column(NUMBER(asdecimal=False), primary_key=True, comment='The payment file received from CheckFree is assigned a number by IB_CheckFreeUpload.')
    recordnumber: Mapped[float] = mapped_column(NUMBER(asdecimal=False), primary_key=True, comment='Represents a row on OSIEXTN.CheckFreeFileRecord.')
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, comment='The run date of the extract.')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='The date the table row was most recently updated.')
    cspid: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment='A unique identifier for the payee, assigned by the CSP.')
    subscriberid: Mapped[Optional[str]] = mapped_column(VARCHAR(55), comment='A unique identifier for the subscriber (assigned by CheckFree).')
    debitacctno: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Account number for the debit account.')
    subscriberfirstname: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment="The subscriber's first name.")
    subscriberlastname: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment="The subscriber's last name.")
    subscribermiddlename: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment="The subscriber's middle name.")
    subscriberaddress1: Mapped[Optional[str]] = mapped_column(VARCHAR(40), comment="First line of the subscriber's mailing address.")
    subscriberaddress2: Mapped[Optional[str]] = mapped_column(VARCHAR(40), comment='Additional mailing address information for the subscriber.')
    subscribercity: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment="The city for the subscriber's address.")
    subscriberstate: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment="The state for the subscriber's address.")
    subscriberzipcd: Mapped[Optional[str]] = mapped_column(VARCHAR(5), comment="The five-digit zip code for the subscriber's address.")
    subscriberzipplus4: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment="The four-digit zip code for the subscriber's address.")
    subscriberzipplus2: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment="The two-digit zip code for the subscriber's address.")
    filetrackid: Mapped[Optional[str]] = mapped_column(VARCHAR(10), comment='Identifies the file from which the payment originated.')
    paymentdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The date the payment should be made based on the request.')
    paymentamount: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='The amount of the payment.')
    paymenttypedescr: Mapped[Optional[str]] = mapped_column(VARCHAR(40), comment='Valid values:P Paper D Draft E Electronic I Internal')
    paymentmatchtypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(3), comment='The method CheckFree uses to match a payment to a standard or managed payee.')
    paymentmatchtypdescr: Mapped[Optional[str]] = mapped_column(VARCHAR(100), comment='The description of payment match type code.')
    standardpayeename: Mapped[Optional[str]] = mapped_column(VARCHAR(35), comment='The payee name assigned to this payment by the subscriber.')
    payeeaddress1: Mapped[Optional[str]] = mapped_column(VARCHAR(40), comment='Mailing address of payee.')
    payeeaddress2: Mapped[Optional[str]] = mapped_column(VARCHAR(40), comment='Additional mailing address information for the payee.')
    payeecity: Mapped[Optional[str]] = mapped_column(VARCHAR(32), comment="The city for the payee's address.")
    payeestate: Mapped[Optional[str]] = mapped_column(VARCHAR(2), comment="The state for the payee's address.")
    payeezipcd: Mapped[Optional[str]] = mapped_column(VARCHAR(5), comment="The five-digit zip code for the payee's address.")
    payeezipplus4: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment="The four-digit zip code extension for the payee's address.")
    payeezipplus2: Mapped[Optional[str]] = mapped_column(VARCHAR(2), comment="The two-digit zip code extension for the payee's address.")
    paymentmethodcd: Mapped[Optional[str]] = mapped_column(VARCHAR(2), comment='The method used to issue the payment.')
    paymentmethoddescr: Mapped[Optional[str]] = mapped_column(VARCHAR(100), comment='The description of the payment method.')
    paymenttransactioncd: Mapped[Optional[str]] = mapped_column(VARCHAR(2), comment='The type of transaction.')
    paymenttransactiondescr: Mapped[Optional[str]] = mapped_column(VARCHAR(100), comment='The description of payment transaction.')
    recurringpaymenttypeind: Mapped[Optional[str]] = mapped_column(VARCHAR(1), comment='Indicates if the payment is a single or recurring payment.')
    ebillautopayindicator: Mapped[Optional[str]] = mapped_column(VARCHAR(1), comment='Indicates if the payment originated from an e-bill automatic payment.Valid values:E E-bill Auto-Pay <space> Payment did not originate from an e-bill Auto-Pay')
    ebillindicator: Mapped[Optional[str]] = mapped_column(VARCHAR(1), comment='Indicates whether the payment is associated with an electronic bill. Valid values: Y Payment is associated with an e-bill N Payment is not associated with an e-bill')
    paymentcategory: Mapped[Optional[str]] = mapped_column(VARCHAR(40), comment="The description of payment's category.")
    checknumber: Mapped[Optional[float]] = mapped_column(NUMBER(8, 0, False), comment='The sequential check number if the payment is processed as a paper check.')
    persnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The system assigned number that identifies every person in Insight.')
    orgnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The system assigned number that identifies every organization in Insight.')
    filecreationdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='Date the file was originally created.')


t_wh_cocc_ofa_ap_bank_accounts = Table(
    'wh_cocc_ofa_ap_bank_accounts', Base.metadata,
    Column('bank_account_id', NUMBER(15, 0, False), nullable=False),
    Column('bank_account_name', VARCHAR(80), nullable=False),
    Column('bank_account_number', VARCHAR(30), nullable=False),
    Column('bank_account_usage', VARCHAR(25)),
    Column('bank_account_type', VARCHAR(25), nullable=False),
    Column('bank_name', VARCHAR(60), nullable=False),
    Column('bank_aba_number', VARCHAR(25)),
    Column('bank_allow_multiple_accounts', VARCHAR(1)),
    Column('bank_account_inactive_date', DateTime),
    Column('org_name', VARCHAR(240), nullable=False),
    Column('bank_account_created_date', DateTime),
    Column('bank_account_created_by', VARCHAR(100), nullable=False),
    Column('rundate', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_cocc_ofa_ap_invoice_dist = Table(
    'wh_cocc_ofa_ap_invoice_dist', Base.metadata,
    Column('distribution_id', NUMBER(15, 0, False), nullable=False),
    Column('distribution_gl_date', DateTime, nullable=False),
    Column('distribution_add_to_assets', VARCHAR(1), nullable=False),
    Column('distribution_line_number', NUMBER(15, 0, False), nullable=False),
    Column('distribution_expense', NUMBER(15, 0, False), nullable=False),
    Column('invoice_id', NUMBER(15, 0, False), nullable=False),
    Column('distribution_type', VARCHAR(25), nullable=False),
    Column('distribution_amount', NUMBER(asdecimal=False)),
    Column('distribution_description', VARCHAR(240)),
    Column('distribution_income_tax_type', VARCHAR(10)),
    Column('distribution_income_tax_region', VARCHAR(10)),
    Column('distribution_tax_name', VARCHAR(15)),
    Column('distribution_status', VARCHAR(40)),
    Column('distribution_accounted', VARCHAR(40)),
    Column('distribution_created_date', DateTime),
    Column('distribution_created_by', VARCHAR(100)),
    Column('rundate', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_cocc_ofa_ap_invoices = Table(
    'wh_cocc_ofa_ap_invoices', Base.metadata,
    Column('invoice_id', NUMBER(15, 0, False), nullable=False),
    Column('vendor_id', NUMBER(15, 0, False), nullable=False),
    Column('vendor_name', VARCHAR(80), nullable=False),
    Column('vendor_site_id', NUMBER(15, 0, False)),
    Column('site_name', VARCHAR(15), nullable=False),
    Column('invoice_number', VARCHAR(50), nullable=False),
    Column('invoice_date', DateTime),
    Column('invoice_amount', NUMBER(asdecimal=False)),
    Column('amount_paid', NUMBER(asdecimal=False)),
    Column('discount_amount', NUMBER(asdecimal=False)),
    Column('invoice_description', VARCHAR(240)),
    Column('invoice_source', VARCHAR(25)),
    Column('invoice_type', VARCHAR(25)),
    Column('invoice_batch', VARCHAR(50), nullable=False),
    Column('invoice_term', VARCHAR(50), nullable=False),
    Column('invoice_pymt_method', VARCHAR(25)),
    Column('invoice_pay_group', VARCHAR(25)),
    Column('invoice_validation_amt', NUMBER(asdecimal=False)),
    Column('invoice_status', VARCHAR(40)),
    Column('org_name', VARCHAR(240), nullable=False),
    Column('invoice_date_created', DateTime),
    Column('invoice_created_by', VARCHAR(100), nullable=False),
    Column('rundate', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_cocc_ofa_ap_payments = Table(
    'wh_cocc_ofa_ap_payments', Base.metadata,
    Column('invoice_payment_id', NUMBER(15, 0, False), nullable=False),
    Column('invoice_id', NUMBER(15, 0, False), nullable=False),
    Column('payment_date', DateTime, nullable=False),
    Column('payment_amount', NUMBER(asdecimal=False), nullable=False),
    Column('bank_account_name', VARCHAR(80), nullable=False),
    Column('bank_account_number', VARCHAR(30), nullable=False),
    Column('payment_method', VARCHAR(25), nullable=False),
    Column('payment_document_name', VARCHAR(20), nullable=False),
    Column('payment_document_number', NUMBER(15, 0, False), nullable=False),
    Column('payment_payee', VARCHAR(240)),
    Column('payment_address_line1', VARCHAR(240)),
    Column('payment_address_line2', VARCHAR(240)),
    Column('payment_address_line3', VARCHAR(240)),
    Column('payment_city', VARCHAR(25)),
    Column('payment_state', VARCHAR(150)),
    Column('payment_zip', VARCHAR(20)),
    Column('payment_date_created', DateTime),
    Column('payment_created_by', VARCHAR(100)),
    Column('ach_payment_bank_aba', VARCHAR(30)),
    Column('ach_payment_account_num', VARCHAR(30)),
    Column('rundate', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_cocc_ofa_ap_vendors = Table(
    'wh_cocc_ofa_ap_vendors', Base.metadata,
    Column('site_id', NUMBER(asdecimal=False), nullable=False),
    Column('vendor_name', VARCHAR(80), nullable=False),
    Column('vendor_number', NUMBER(asdecimal=False)),
    Column('tax_id_num', VARCHAR(30)),
    Column('tax_type', VARCHAR(10)),
    Column('tax_name_control', VARCHAR(4)),
    Column('tax_org_type', VARCHAR(25)),
    Column('reportable_fed', VARCHAR(1)),
    Column('reportable_state', VARCHAR(1)),
    Column('site_name', VARCHAR(15)),
    Column('address_line_1', VARCHAR(240)),
    Column('address_line_2', VARCHAR(240)),
    Column('address_line_3', VARCHAR(240)),
    Column('city', VARCHAR(25)),
    Column('state', VARCHAR(25)),
    Column('zip', VARCHAR(20)),
    Column('province', VARCHAR(25)),
    Column('country', VARCHAR(25)),
    Column('phone_number', VARCHAR(25)),
    Column('fax_number', VARCHAR(25)),
    Column('contact_name', VARCHAR(50)),
    Column('contact_phone', VARCHAR(25)),
    Column('bank_name', VARCHAR(60)),
    Column('bank_account_name', VARCHAR(80)),
    Column('bank_account_number', VARCHAR(30)),
    Column('payment_method', VARCHAR(25)),
    Column('distribution_set_name', VARCHAR(50)),
    Column('pay_group', VARCHAR(25)),
    Column('payment_priority', NUMBER(asdecimal=False)),
    Column('hold_payments', VARCHAR(1)),
    Column('terms', VARCHAR(50), nullable=False),
    Column('tax_address', VARCHAR(1)),
    Column('org_name', VARCHAR(240)),
    Column('vendor_site_creation_date', DateTime),
    Column('vendor_site_created_by', VARCHAR(100), nullable=False),
    Column('inactive_vendors', DateTime),
    Column('inactive_sites', DateTime),
    Column('rundate', DateTime),
    schema='COCCDM'
)


t_wh_cocc_ofa_gl_balances = Table(
    'wh_cocc_ofa_gl_balances', Base.metadata,
    Column('code_combination_id', NUMBER(15, 0, False), nullable=False),
    Column('acct_combination', VARCHAR(77), nullable=False),
    Column('company_number', VARCHAR(25)),
    Column('account_number', VARCHAR(25)),
    Column('dept_number', VARCHAR(25)),
    Column('currency_code', VARCHAR(15), nullable=False),
    Column('period_name', VARCHAR(15), nullable=False),
    Column('period_year', NUMBER(15, 0, False), nullable=False),
    Column('period_number', NUMBER(15, 0, False), nullable=False),
    Column('bal_actual_mtd', NUMBER(asdecimal=False)),
    Column('bal_actual_calendar_qtd', NUMBER(asdecimal=False)),
    Column('bal_actual_fiscal_qtd', NUMBER(asdecimal=False)),
    Column('bal_actual_calendar_ytd', NUMBER(asdecimal=False)),
    Column('bal_actual_fiscal_ytd', NUMBER(asdecimal=False)),
    Column('bal_average_mtd', NUMBER(asdecimal=False)),
    Column('bal_average_calendar_qtd', NUMBER(asdecimal=False)),
    Column('bal_average_fiscal_qtd', NUMBER(asdecimal=False)),
    Column('bal_average_calendar_ytd', NUMBER(asdecimal=False)),
    Column('bal_average_fiscal_ytd', NUMBER(asdecimal=False)),
    Column('bal_budget_mtd', NUMBER(asdecimal=False)),
    Column('bal_budget_calendar_qtd', NUMBER(asdecimal=False)),
    Column('bal_budget_fiscal_qtd', NUMBER(asdecimal=False)),
    Column('bal_budget_calendar_ytd', NUMBER(asdecimal=False)),
    Column('bal_budget_fiscal_ytd', NUMBER(asdecimal=False)),
    Column('last_updated_by', VARCHAR(100)),
    Column('last_update_date', DateTime),
    Column('effdate', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_cocc_ofa_gl_balances_hist = Table(
    'wh_cocc_ofa_gl_balances_hist', Base.metadata,
    Column('code_combination_id', NUMBER(15, 0, False), nullable=False),
    Column('acct_combination', VARCHAR(77), nullable=False),
    Column('company_number', VARCHAR(25)),
    Column('account_number', VARCHAR(25)),
    Column('dept_number', VARCHAR(25)),
    Column('currency_code', VARCHAR(15), nullable=False),
    Column('period_name', VARCHAR(15), nullable=False),
    Column('period_year', NUMBER(15, 0, False), nullable=False),
    Column('period_number', NUMBER(15, 0, False), nullable=False),
    Column('bal_actual_mtd', NUMBER(asdecimal=False)),
    Column('bal_actual_calendar_qtd', NUMBER(asdecimal=False)),
    Column('bal_actual_fiscal_qtd', NUMBER(asdecimal=False)),
    Column('bal_actual_calendar_ytd', NUMBER(asdecimal=False)),
    Column('bal_actual_fiscal_ytd', NUMBER(asdecimal=False)),
    Column('bal_average_mtd', NUMBER(asdecimal=False)),
    Column('bal_average_calendar_qtd', NUMBER(asdecimal=False)),
    Column('bal_average_fiscal_qtd', NUMBER(asdecimal=False)),
    Column('bal_average_calendar_ytd', NUMBER(asdecimal=False)),
    Column('bal_average_fiscal_ytd', NUMBER(asdecimal=False)),
    Column('bal_budget_mtd', NUMBER(asdecimal=False)),
    Column('bal_budget_calendar_qtd', NUMBER(asdecimal=False)),
    Column('bal_budget_fiscal_qtd', NUMBER(asdecimal=False)),
    Column('bal_budget_calendar_ytd', NUMBER(asdecimal=False)),
    Column('bal_budget_fiscal_ytd', NUMBER(asdecimal=False)),
    Column('last_updated_by', VARCHAR(100)),
    Column('last_update_date', DateTime),
    Column('effdate', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_cocc_ofa_gl_balances_temp = Table(
    'wh_cocc_ofa_gl_balances_temp', Base.metadata,
    Column('code_combination_id', NUMBER(15, 0, False), nullable=False),
    Column('acct_combination', VARCHAR(77), nullable=False),
    Column('company_number', VARCHAR(25)),
    Column('account_number', VARCHAR(25)),
    Column('dept_number', VARCHAR(25)),
    Column('currency_code', VARCHAR(15), nullable=False),
    Column('period_name', VARCHAR(15), nullable=False),
    Column('period_year', NUMBER(15, 0, False), nullable=False),
    Column('period_number', NUMBER(15, 0, False), nullable=False),
    Column('bal_actual_mtd', NUMBER(asdecimal=False)),
    Column('bal_actual_calendar_qtd', NUMBER(asdecimal=False)),
    Column('bal_actual_fiscal_qtd', NUMBER(asdecimal=False)),
    Column('bal_actual_calendar_ytd', NUMBER(asdecimal=False)),
    Column('bal_actual_fiscal_ytd', NUMBER(asdecimal=False)),
    Column('bal_average_mtd', NUMBER(asdecimal=False)),
    Column('bal_average_calendar_qtd', NUMBER(asdecimal=False)),
    Column('bal_average_fiscal_qtd', NUMBER(asdecimal=False)),
    Column('bal_average_calendar_ytd', NUMBER(asdecimal=False)),
    Column('bal_average_fiscal_ytd', NUMBER(asdecimal=False)),
    Column('bal_budget_mtd', NUMBER(asdecimal=False)),
    Column('bal_budget_calendar_qtd', NUMBER(asdecimal=False)),
    Column('bal_budget_fiscal_qtd', NUMBER(asdecimal=False)),
    Column('bal_budget_calendar_ytd', NUMBER(asdecimal=False)),
    Column('bal_budget_fiscal_ytd', NUMBER(asdecimal=False)),
    Column('last_updated_by', VARCHAR(100)),
    Column('last_update_date', DateTime),
    Column('effdate', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_cocc_ofa_gl_glchart = Table(
    'wh_cocc_ofa_gl_glchart', Base.metadata,
    Column('code_combination_id', NUMBER(15, 0, False), nullable=False),
    Column('acct_combination', VARCHAR(77), nullable=False),
    Column('account_type', VARCHAR(1), nullable=False),
    Column('company_number', VARCHAR(25)),
    Column('account_number', VARCHAR(25)),
    Column('dept_number', VARCHAR(25)),
    Column('company_description', VARCHAR(240)),
    Column('account_description', VARCHAR(240)),
    Column('dept_description', VARCHAR(240)),
    Column('posting_allowed_yn', VARCHAR(1), nullable=False),
    Column('budgeting_allowed_yn', VARCHAR(1), nullable=False),
    Column('combination_enabled_yn', VARCHAR(1), nullable=False),
    Column('effective_from', DateTime),
    Column('effective_to', DateTime),
    Column('elimination_yn', VARCHAR(1)),
    Column('last_updated_by', VARCHAR(100)),
    Column('last_update_date', DateTime),
    Column('segment1_value_enabled_yn', VARCHAR(1)),
    Column('segment2_value_enabled_yn', VARCHAR(1)),
    Column('segment3_value_enabled_yn', VARCHAR(1)),
    Column('effdate', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_cocc_ofa_gl_journals = Table(
    'wh_cocc_ofa_gl_journals', Base.metadata,
    Column('posted_date', DateTime),
    Column('effective_date', DateTime),
    Column('code_combination_id', NUMBER(15, 0, False), nullable=False),
    Column('acct_combination', VARCHAR(77), nullable=False),
    Column('account_type', VARCHAR(1), nullable=False),
    Column('company_number', VARCHAR(25)),
    Column('account_number', VARCHAR(25)),
    Column('dept_number', VARCHAR(25)),
    Column('currency_code', VARCHAR(15), nullable=False),
    Column('je_status', VARCHAR(1)),
    Column('amount', NUMBER(asdecimal=False)),
    Column('tran_description', VARCHAR(240)),
    Column('je_source', VARCHAR(25)),
    Column('je_category', VARCHAR(25)),
    Column('ap_vendor', VARCHAR(240)),
    Column('ap_invoice_number', VARCHAR(240)),
    Column('created_by', VARCHAR(100)),
    Column('last_update_date', DateTime),
    Column('effdate', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_cocc_ofa_gl_journals_temp = Table(
    'wh_cocc_ofa_gl_journals_temp', Base.metadata,
    Column('posted_date', DateTime),
    Column('effective_date', DateTime),
    Column('code_combination_id', NUMBER(15, 0, False), nullable=False),
    Column('acct_combination', VARCHAR(77), nullable=False),
    Column('account_type', VARCHAR(1), nullable=False),
    Column('company_number', VARCHAR(25)),
    Column('account_number', VARCHAR(25)),
    Column('dept_number', VARCHAR(25)),
    Column('currency_code', VARCHAR(15), nullable=False),
    Column('je_status', VARCHAR(1)),
    Column('amount', NUMBER(asdecimal=False)),
    Column('tran_description', VARCHAR(240)),
    Column('je_source', VARCHAR(25)),
    Column('je_category', VARCHAR(25)),
    Column('ap_vendor', VARCHAR(240)),
    Column('ap_invoice_number', VARCHAR(240)),
    Column('created_by', VARCHAR(100)),
    Column('last_update_date', DateTime),
    Column('effdate', DateTime, nullable=False),
    schema='COCCDM'
)


class WhCommon(Base):
    __tablename__ = 'wh_common'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rundate', name='wh_common_pk'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    firstname: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    mdlname: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    lastname: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    datebirth: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    allotmentyn: Mapped[Optional[str]] = mapped_column(CHAR(1), server_default=text("'n'"))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class WhCommonMe(Base):
    __tablename__ = 'wh_common_me'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rundate', name='sys_c_snap$_3wh_common_temp_p'),
        Index('wh_common_me_dx1', 'acctnbr'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    firstname: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    mdlname: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    lastname: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    datebirth: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    allotmentyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class WhCommonTemp(Base):
    __tablename__ = 'wh_common_temp'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rundate', name='wh_common_temp_pk'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    firstname: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    mdlname: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    lastname: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    datebirth: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    allotmentyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


t_wh_contact_events = Table(
    'wh_contact_events', Base.metadata,
    Column('contacteventnbr', NUMBER(22, 0, False), comment='The unique identifier of each contact record on a person or organization.'),
    Column('contacteventtypcd', VARCHAR(4), comment='The Contact Event Type Code is the type associated with the Contact.'),
    Column('contacteventtypdesc', VARCHAR(30), comment='The description of the event type'),
    Column('contactpersnbr', NUMBER(22, 0, False), comment='The Contact Person Number is the person linked with the contact.'),
    Column('contactpersname', VARCHAR(50), comment='The Contact Person Name is the person linked with the contact'),
    Column('contactorgnbr', NUMBER(22, 0, False), comment='The Contact Organization Number is the organization linked with the contact.'),
    Column('contactorgname', VARCHAR(50), comment='The Contact Organization Name is the organization linked with the contact.'),
    Column('dateopened', DateTime, comment='The Date Opened is the date the contact is created.'),
    Column('duedate', DateTime, comment='The Due Date is the date the contact resolution is due.'),
    Column('contactacctnbr', NUMBER(22, 0, False), comment='The Contact Account Number is the account linked with the contact.'),
    Column('dateresolved', DateTime, comment='The Resolved Date is the date the contact is resolved.'),
    Column('contacteventstatcd', VARCHAR(4), comment='The Current Contact Status Code identifies the current status of the contact.'),
    Column('contacteventstatdesc', VARCHAR(30), comment='The Contact Event Status Description contains the textual description of the contact status.'),
    Column('designateasopenyn', CHAR(1), nullable=False, server_default=text("'N' "), comment='The Designate As Open identifies if the status is designated as open or close.'),
    Column('createpersnbr', NUMBER(22, 0, False), comment='The Create Person Number identifies the person who created the contact.'),
    Column('createpersname', VARCHAR(50), comment='The Create Person Name identifies the person who created the contact.'),
    Column('assignpersnbr', NUMBER(22, 0, False), comment='The Assign Person Number identifies the person to whom the contact is assigned.'),
    Column('assignpersname', VARCHAR(50), comment='The Assign Person Name identifies the person to whom the contact is assigned.'),
    Column('rundate', DateTime, comment='The date report is run'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM  USE  ONLY'),
    schema='COCCDM'
)


t_wh_contact_notes = Table(
    'wh_contact_notes', Base.metadata,
    Column('contacteventnbr', NUMBER(22, 0, False), nullable=False, comment='The Contact Event Number is the number that identifies the contact.'),
    Column('notenbr', NUMBER(22, 0, False), nullable=False, comment='The Note Number is the system assigned number that uniquely identifies each note.'),
    Column('createdate', DateTime, nullable=False, comment='The Create Date is the date the note was created.'),
    Column('createpersnbr', NUMBER(22, 0, False), nullable=False, comment='The Create Person Number identifies the person who created the note.'),
    Column('createpersname', VARCHAR(40), nullable=False),
    Column('inactivedate', DateTime, comment='The Inactive Date is the date the note is inactive.'),
    Column('notetext', VARCHAR(1500), nullable=False, comment='The Note Text is the textual detail of the note.'),
    Column('rundate', DateTime, nullable=False, comment='The rundate of the queue'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM  USE  ONLY'),
    schema='COCCDM'
)


t_wh_contact_status_history = Table(
    'wh_contact_status_history', Base.metadata,
    Column('contacteventnbr', NUMBER(22, 0, False), comment='The Contact Event Number is the number that identifies the contact.'),
    Column('effdatetime', DateTime, comment='The Effective Date is the year, month and day that the status change is effective.'),
    Column('contacteventstatcd', VARCHAR(4), comment='The Contact Event Status Code is the status code for the contact during this time period.'),
    Column('contacteventstatdesc', VARCHAR(30), comment='The status change description is the note added while changing the status.'),
    Column('statuschgdesc', VARCHAR(200), comment='The Status Change Description is the note added while changing the status.'),
    Column('rundate', DateTime, comment='The date of the batch run'),
    Column('contactdatelastmaint', DateTime, comment='The date of the maintenance'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date of the maintenance'),
    schema='COCCDM'
)


t_wh_creditcip = Table(
    'wh_creditcip', Base.metadata,
    Column('orgnbr', NUMBER(22, 0, False), comment='The organization number is the system assigned number used to identify each organization.'),
    Column('persnbr', NUMBER(22, 0, False), comment='The person number is the system assigned number that identifies every person.'),
    Column('rundate', DateTime, comment='Post Date when job was run.'),
    Column('scoredate', DateTime, comment='The date the credit score was determined.'),
    Column('creditscore', NUMBER(15, 0, False), comment='The numeric value assigned to rate the ability to repay a debit.'),
    Column('cipratingcd', VARCHAR(4), comment='The cip rating code identifies the user defined codes used for person ratings.'),
    Column('cipratingdate', DateTime, comment='The effective date is the date that the cip rating is effective.'),
    Column('nextcipratingdate', DateTime, comment='The next cip rating date is the date when the next cip rating is to be done.'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date last maintenance is the date when this row was most recently updated. System use only.'),
    schema='COCCDM'
)


class WhDeposit(Base):
    __tablename__ = 'wh_deposit'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rundate', name='wh_deposit_pk'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    sw: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    atm: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    eft: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    mailcode: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    retirement: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    mtdamtint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    directdepyn: Mapped[Optional[str]] = mapped_column(CHAR(1), server_default=text("'n'"))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ytdavgbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True))
    billpayflag: Mapped[Optional[str]] = mapped_column(VARCHAR(1))


class WhDepositMe(Base):
    __tablename__ = 'wh_deposit_me'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rundate', name='sys_c_snap$_5wh_deposit_temp_'),
        Index('wh_deposit_me_dx1', 'acctnbr'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    sw: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    atm: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    eft: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    mailcode: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    retirement: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    mtdamtint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    directdepyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ytdavgbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True))
    billpayflag: Mapped[Optional[str]] = mapped_column(VARCHAR(1))


class WhDepositTemp(Base):
    __tablename__ = 'wh_deposit_temp'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rundate', name='wh_deposit_temp_pk'),
        Index('wh_deposit_temp_dx1', 'acctnbr'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    sw: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    atm: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    eft: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    mailcode: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    retirement: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    mtdamtint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    directdepyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ytdavgbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True))
    billpayflag: Mapped[Optional[str]] = mapped_column(VARCHAR(1))


t_wh_inspolicy = Table(
    'wh_inspolicy', Base.metadata,
    Column('intrpolicynbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('insorgnbr', NUMBER(22, 0, False)),
    Column('instypcd', VARCHAR(4)),
    Column('extpolicynbr', VARCHAR(30)),
    Column('agentorgnbr', NUMBER(22, 0, False)),
    Column('premcalperiodcd', VARCHAR(4)),
    Column('premamt', NUMBER(12, 2, True)),
    Column('effdate', DateTime),
    Column('expiredate', DateTime),
    Column('policydocnbr', NUMBER(22, 0, False)),
    Column('inactivedate', DateTime),
    Column('firstmonthcd', VARCHAR(4)),
    Column('duedaynbr', NUMBER(22, 0, False)),
    Column('dueweekdaycd', VARCHAR(4)),
    Column('coverageamt', NUMBER(22, 5, True)),
    Column('firstyearnbr', NUMBER(22, 0, False)),
    Column('refundableyn', CHAR(1), nullable=False),
    Column('instypdesc', VARCHAR(30)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_invr = Table(
    'wh_invr', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False),
    Column('acctgrpnbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('invrstatcd', VARCHAR(4)),
    Column('invracctnbr', VARCHAR(22)),
    Column('soldamt', NUMBER(22, 5, True)),
    Column('firstpmtsolddate', DateTime),
    Column('pctowned', NUMBER(8, 7, True)),
    Column('originvrrate', NUMBER(8, 7, True)),
    Column('servfeeratemethcd', VARCHAR(4)),
    Column('servfeepct', NUMBER(8, 7, True)),
    Column('servfeeamt', NUMBER(22, 5, True)),
    Column('noteholdercd', VARCHAR(4)),
    Column('nextratechangedate', DateTime),
    Column('nonstdrepmtyn', CHAR(1), nullable=False),
    Column('inactivedate', DateTime),
    Column('solddate', DateTime),
    Column('currinvrrate', NUMBER(8, 7, True)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_invraction = Table(
    'wh_invraction', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False),
    Column('acctgrpnbr', NUMBER(22, 0, False), nullable=False),
    Column('effdate', DateTime, nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('actioncd', VARCHAR(4)),
    Column('actiondesc', VARCHAR(30)),
    Column('actionvalue', VARCHAR(30)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_invrloanprogram = Table(
    'wh_invrloanprogram', Base.metadata,
    Column('acctgrpnbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('invrlpcd', VARCHAR(4), nullable=False),
    Column('remittypcd', VARCHAR(4), nullable=False),
    Column('remitmethcd', VARCHAR(4)),
    Column('remitdays', NUMBER(22, 0, False)),
    Column('createallotyn', CHAR(1), nullable=False),
    Column('oddduedateasisyn', CHAR(1), nullable=False),
    Column('payoffremitdays', NUMBER(22, 0, False)),
    Column('invrlpdesc', VARCHAR(30)),
    Column('releasedyn', CHAR(1), nullable=False),
    Column('nonstdrepmtyn', CHAR(1), nullable=False),
    Column('remittypdesc', VARCHAR(30)),
    Column('mbsyn', CHAR(1), nullable=False),
    Column('mrsyn', CHAR(1), nullable=False),
    Column('remitintyn', CHAR(1), nullable=False),
    Column('remitprinyn', CHAR(1), nullable=False),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_invrratechg = Table(
    'wh_invrratechg', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False),
    Column('acctgrpnbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('ratechangecalpercd', VARCHAR(4)),
    Column('calperioddesc', VARCHAR(30)),
    Column('ratechangewithloanyn', CHAR(1), nullable=False),
    Column('raterecalcmethcd', VARCHAR(4)),
    Column('raterecalcmethdesc', VARCHAR(30)),
    Column('calcschednbr', NUMBER(22, 0, False)),
    Column('calcschedname', VARCHAR(30)),
    Column('ratechangeleaddays', NUMBER(22, 0, False)),
    Column('marginpct', NUMBER(8, 7, True)),
    Column('rndmethcd', VARCHAR(4)),
    Column('rndmethdesc', VARCHAR(30)),
    Column('maxratechangeperreview', NUMBER(8, 7, True)),
    Column('mininvrate', NUMBER(8, 7, True)),
    Column('maxinvrate', NUMBER(8, 7, True)),
    Column('guarnservspreadpct', NUMBER(8, 7, True)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_lien = Table(
    'wh_lien', Base.metadata,
    Column('liennbr', NUMBER(22, 0, False)),
    Column('acctnbr', NUMBER(22, 0, False)),
    Column('rundate', DateTime, nullable=False),
    Column('propnbr', NUMBER(22, 0, False)),
    Column('lientypcd', VARCHAR(4)),
    Column('liendesc', VARCHAR(30)),
    Column('persnbr', NUMBER(22, 0, False)),
    Column('orgnbr', NUMBER(22, 0, False)),
    Column('nbroflien', NUMBER(22, 0, False)),
    Column('lienamt', NUMBER(15, 2, True)),
    Column('liableyn', CHAR(1), nullable=False),
    Column('inactivedate', DateTime),
    Column('filedate', DateTime),
    Column('fileorgnbr', NUMBER(22, 0, False)),
    Column('daterelease', DateTime),
    Column('lientypdesc', VARCHAR(30)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


class WhLoans(Base):
    __tablename__ = 'wh_loans'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rundate', name='wh_loans_pk'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    occ: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    status: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    origbal: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    currterm: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    intc: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    pf: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    delyr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    dellife: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    lcrate: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    oldpi: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    origint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    nextratechg: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    loanidx: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    rcf: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    pcf: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    remainterm: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    lastpmtchgdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    lastintchgdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    sold: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(24, 10, True))
    soldbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    grossbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    holdback: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    ratechangeleaddays: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    principaladvamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True))
    refinanceamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True))
    origdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    fdiccatdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    otsloancatdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    lastdisbursdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    intpaidtodate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    fhlbpledgedyn: Mapped[Optional[str]] = mapped_column(CHAR(1), comment='Pledgedyn identifies if the loan is pledged to the loan account.')
    fhlbclattypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies the collateral type of the current loan for the fhlb organization.')
    fhlbclasscd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies the collateral class of the current loan for the fhlb organization.')
    fhlbindexcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies the index of the current loan for the fhlb organization.')
    fhlbratecapcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies the rate cap of the current loan for the fhlb organization.')
    fhlbfreqrateadjcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies the frequency rate adjustment of the current loan for the fhlb organization.')
    fhlb1strateadjcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies the 1st rate adjustment of the current loan for the fhlb organization.')
    loanlimityn: Mapped[Optional[str]] = mapped_column(CHAR(1), comment='Determines if this account is a Line of Credit Loan.')
    revolveloanyn: Mapped[Optional[str]] = mapped_column(CHAR(1), comment='Determines if this a revolving line Account.')
    availbalamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True), comment='The Available Amount column identifies the amount of funds that will be available.')


class WhLoansMe(Base):
    __tablename__ = 'wh_loans_me'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rundate', name='sys_c_snap$_7wh_loans_temp_pk'),
        Index('wh_loans_me_dx1', 'acctnbr'),
        Index('wh_loans_me_dx10', 'fhlb1strateadjcd'),
        Index('wh_loans_me_dx2', 'status'),
        Index('wh_loans_me_dx3', 'rcf'),
        Index('wh_loans_me_dx4', 'pcf'),
        Index('wh_loans_me_dx5', 'fhlbclattypcd'),
        Index('wh_loans_me_dx6', 'fhlbclasscd'),
        Index('wh_loans_me_dx7', 'fhlbindexcd'),
        Index('wh_loans_me_dx8', 'fhlbratecapcd'),
        Index('wh_loans_me_dx9', 'fhlbfreqrateadjcd'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    occ: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    status: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    origbal: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    currterm: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    intc: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    pf: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    delyr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    dellife: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    lcrate: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    oldpi: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    origint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    nextratechg: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    loanidx: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    rcf: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    pcf: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    remainterm: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    lastpmtchgdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    lastintchgdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    sold: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(24, 10, True))
    soldbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    grossbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    holdback: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    ratechangeleaddays: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    principaladvamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True))
    refinanceamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True))
    origdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    fdiccatdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    otsloancatdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    lastdisbursdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    intpaidtodate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    fhlbpledgedyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    fhlbclattypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    fhlbclasscd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    fhlbindexcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    fhlbratecapcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    fhlbfreqrateadjcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    fhlb1strateadjcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    loanlimityn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    revolveloanyn: Mapped[Optional[str]] = mapped_column(CHAR(1))
    availbalamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True))


class WhLoansTemp(Base):
    __tablename__ = 'wh_loans_temp'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rundate', name='wh_loans_temp_pk'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True)
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    occ: Mapped[Optional[str]] = mapped_column(VARCHAR(1))
    status: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    origbal: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    currterm: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    intc: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    pf: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    delyr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    dellife: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    lcrate: Mapped[Optional[str]] = mapped_column(VARCHAR(128))
    oldpi: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    origint: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 7, True))
    nextratechg: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    loanidx: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    rcf: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    pcf: Mapped[Optional[str]] = mapped_column(VARCHAR(4))
    remainterm: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    lastpmtchgdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    lastintchgdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    sold: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(24, 10, True))
    soldbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    grossbal: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    holdback: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True))
    ratechangeleaddays: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False))
    principaladvamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True))
    refinanceamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 5, True))
    origdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    fdiccatdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    otsloancatdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    lastdisbursdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datelastmaint: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    intpaidtodate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    fhlbpledgedyn: Mapped[Optional[str]] = mapped_column(CHAR(1), comment='Pledgedyn identifies if the loan is pledged to the loan account.')
    fhlbclattypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies the collateral type of the current loan for the fhlb organization.')
    fhlbclasscd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies the collateral class of the current loan for the fhlb organization.')
    fhlbindexcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies the index of the current loan for the fhlb organization.')
    fhlbratecapcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies the rate cap of the current loan for the fhlb organization.')
    fhlbfreqrateadjcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies the frequency rate adjustment of the current loan for the fhlb organization.')
    fhlb1strateadjcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies the 1st rate adjustment of the current loan for the fhlb organization.')
    loanlimityn: Mapped[Optional[str]] = mapped_column(CHAR(1), comment='Determines if this account is a Line of Credit Loan.')
    revolveloanyn: Mapped[Optional[str]] = mapped_column(CHAR(1), comment='Determines if this a revolving line Account.')
    availbalamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True), comment='The Available Amount column identifies the amount of funds that will be available.')


t_wh_maint = Table(
    'wh_maint', Base.metadata,
    Column('actvnbr', NUMBER(22, 0, False), comment='The Activity Number is the system assigned number.'),
    Column('actvcatcd', VARCHAR(4), comment='The Activity Category Code is the user defined code used to identify the activity category.'),
    Column('actvcatdesc', VARCHAR(30), comment='The Activity Category Description is the textual description of the activity.'),
    Column('actvtypcd', VARCHAR(4), comment='The Activity Type Code is the user defined code used to define the type of activity.'),
    Column('actvtypdesc', VARCHAR(60), comment='The Activity Type Description contains the textual description of the activity.'),
    Column('parentactvnbr', NUMBER(22, 0, False), comment='The Parent Activity Number column identifies the parent account for the activity.'),
    Column('actvdesc', VARCHAR(30), comment='The Activity Description is the textual description of the activity.'),
    Column('resppersnbr', NUMBER(22, 0, False), comment='The Responsible Person Number for the activity.'),
    Column('resppersname', VARCHAR(40), comment='The Responsible Person Name for the activity.'),
    Column('apprpersnbr', NUMBER(22, 0, False), comment='The Approval Person number for the activity.'),
    Column('apprpersname', VARCHAR(40), comment='The Approval Person Name for the activity.'),
    Column('databaseactvcd', VARCHAR(6), comment='The Data Base Activity Code is the code which identifies the activity.'),
    Column('acctnbr', NUMBER(22, 0, False), comment='The Subject Account Number for the activity.'),
    Column('persnbr', NUMBER(22, 0, False), comment='The Subject Person Number for the activity.'),
    Column('persname', VARCHAR(40), comment='The Subject Person Name for the person.'),
    Column('orgnbr', NUMBER(22, 0, False), comment='The Subject Organization Number for the activity.'),
    Column('orgname', VARCHAR(60), comment='The Subject Organization Name for the activity.'),
    Column('tableid', VARCHAR(30), comment='The Table ID is the table that was changed with the activity.'),
    Column('columnid', VARCHAR(30), comment='The Column ID is the column name pertaining to the activity.'),
    Column('oldvalue', VARCHAR(60), comment='The Old Value is the value before the activity.'),
    Column('newvalue', VARCHAR(60), comment='The New Value is the value after the activity.'),
    Column('maintdate', DateTime, comment='The MAINTDATE is the date when this row was most recently updated.'),
    Column('ovrdnotenbr', NUMBER(22, 0, False), comment='The Override Note Number is the number of the note associated with the override.'),
    Column('ovrdnote', VARCHAR(200), comment='The Note Text is the textual detail of the note.'),
    Column('applnbr', NUMBER(22, 0, False), comment='Uniquely identifies the row for each application row in this table.'),
    Column('appldesc', VARCHAR(60), comment='Provides a short text description or title of the application.'),
    Column('rundate', DateTime, comment='The date when the batch queue was run.'),
    Column('datelastmaint', DateTime, server_default=text('SYSDATE')),
    schema='COCCDM'
)


t_wh_maint_temp = Table(
    'wh_maint_temp', Base.metadata,
    Column('actvnbr', NUMBER(22, 0, False), comment='The Activity Number is the system assigned number.'),
    Column('actvcatcd', VARCHAR(4), comment='The Activity Category Code is the user defined code used to identify the activity category.'),
    Column('actvcatdesc', VARCHAR(30), comment='The Activity Category Description is the textual description of the activity.'),
    Column('actvtypcd', VARCHAR(4), comment='The Activity Type Code is the user defined code used to define the type of activity.'),
    Column('actvtypdesc', VARCHAR(60), comment='The Activity Type Description contains the textual description of the activity.'),
    Column('parentactvnbr', NUMBER(22, 0, False), comment='The Parent Activity Number column identifies the parent account for the activity.'),
    Column('actvdesc', VARCHAR(30), comment='The Activity Description is the textual description of the activity.'),
    Column('resppersnbr', NUMBER(22, 0, False), comment='The Responsible Person Number for the activity.'),
    Column('resppersname', VARCHAR(40), comment='The Responsible Person Name for the activity.'),
    Column('apprpersnbr', NUMBER(22, 0, False), comment='The Approval Person number for the activity.'),
    Column('apprpersname', VARCHAR(40), comment='The Approval Person Name for the activity.'),
    Column('databaseactvcd', VARCHAR(6), comment='The Data Base Activity Code is the code which identifies the activity.'),
    Column('acctnbr', NUMBER(22, 0, False), comment='The Subject Account Number for the activity.'),
    Column('persnbr', NUMBER(22, 0, False), comment='The Subject Person Number for the activity.'),
    Column('persname', VARCHAR(40), comment='The Subject Person Name for the person.'),
    Column('orgnbr', NUMBER(22, 0, False), comment='The Subject Organization Number for the activity.'),
    Column('orgname', VARCHAR(60), comment='The Subject Organization Name for the activity.'),
    Column('tableid', VARCHAR(30), comment='The Table ID is the table that was changed with the activity.'),
    Column('columnid', VARCHAR(30), comment='The Column ID is the column name pertaining to the activity.'),
    Column('oldvalue', VARCHAR(60), comment='The Old Value is the value before the activity.'),
    Column('newvalue', VARCHAR(60), comment='The New Value is the value after the activity.'),
    Column('maintdate', DateTime, comment='The MAINTDATE is the date when this row was most recently updated.'),
    Column('ovrdnotenbr', NUMBER(22, 0, False), comment='The Override Note Number is the number of the note associated with the override.'),
    Column('ovrdnote', VARCHAR(200), comment='The Note Text is the textual detail of the note.'),
    Column('applnbr', NUMBER(22, 0, False), comment='Uniquely identifies the row for each application row in this table.'),
    Column('appldesc', VARCHAR(60), comment='Provides a short text description or title of the application.'),
    Column('rundate', DateTime, comment='The date when the batch queue was run.'),
    Column('datelastmaint', DateTime, server_default=text('SYSDATE')),
    schema='COCCDM'
)


t_wh_masterline = Table(
    'wh_masterline', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False),
    Column('acctgrpnbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('acctgrptypcd', VARCHAR(4), nullable=False),
    Column('memolimitamt', NUMBER(22, 5, True)),
    Column('memolimiteffdate', DateTime),
    Column('memolimitinactivedate', DateTime),
    Column('masteracctyn', CHAR(1), nullable=False),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_org = Table(
    'wh_org', Base.metadata,
    Column('orgnbr', NUMBER(22, 0, False), comment='The Organization Number is the system assigned number used to identify each organization.'),
    Column('orgname', VARCHAR(60), comment='The Organization Name is the legal name for the organization.'),
    Column('orgtypcd', VARCHAR(4), comment='The Organization Type Code is the user assigned value that identifies the valid organization types.'),
    Column('orgtypcddesc', VARCHAR(30), comment='The Organization Type Description is the textual description of the organization type codes.'),
    Column('taxid', VARCHAR(60), comment='The Tax ID is the tax identification number for the organization.'),
    Column('taxidtypcd', VARCHAR(4), comment='The Tax ID Type Code is a user assigned code that identifies the tax ID types.'),
    Column('rpt1099intyn', VARCHAR(1), comment='The Report 1099 Interest Y=Yes N=No determines if the interest paid is to be reported for the organization.'),
    Column('privacyyn', VARCHAR(1), comment='The Privacy Code represents the ability to release information pertaining to this organization.'),
    Column('taxexemptyn', VARCHAR(1), comment='Yes/no indicator specifies whether or not the organization is tax exempt.'),
    Column('cipratingcd', VARCHAR(4), comment='CIPRATINGCD is the CIP Rating code for the organization.'),
    Column('creditscore', NUMBER(15, 0, False), comment='The numeric value assigned to rate the ability to repay a debit.'),
    Column('siccd', VARCHAR(4), comment='The SIC Code is the user assigned code that identifies the standard industrial class for the organization.'),
    Column('siccddesc', VARCHAR(60), comment='The SIC Description is the textual description of the standard industrial class.'),
    Column('sicsubcd', VARCHAR(4), comment='The SIC Sub Code is is a user assigned code that identifies the standard industrial class sub that applies to an organization.'),
    Column('sicsubcddesc', VARCHAR(60), comment='The SIC Subordinate Description is the textual description of the standard industry class subordinate codes.'),
    Column('naicscd', VARCHAR(6), comment='The government assigned NAICS industry class code.'),
    Column('naicscddesc', VARCHAR(254), comment='The government assigned NAICS industry description.'),
    Column('adddate', DateTime, comment='The Add Date is the date the organization was added to the system.'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM  USE  ONLY'),
    Column('rundate', DateTime, comment='The date report is run'),
    Column('homeemail', VARCHAR(40)),
    Column('busemail', VARCHAR(40)),
    Column('allowpromoyn', VARCHAR(1), comment='Determines if promo calls and messages are allowed'),
    schema='COCCDM'
)


t_wh_orgpersrole = Table(
    'wh_orgpersrole', Base.metadata,
    Column('orgnbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('persrolecd', VARCHAR(4)),
    Column('persnbr', NUMBER(22, 0, False)),
    Column('persroledesc', VARCHAR(30)),
    Column('orgrolecd', VARCHAR(4)),
    Column('subjorgnbr', NUMBER(22, 0, False)),
    Column('orgroledesc', VARCHAR(30)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_orguserfields = Table(
    'wh_orguserfields', Base.metadata,
    Column('orgnbr', NUMBER(22, 0, False), nullable=False, comment='The Organization Number is a system-assigned primary key that uniquely identifies the organization. '),
    Column('orguserfieldcd', VARCHAR(4), comment='The Organization User Field Code is the user field code associated with the organization. '),
    Column('orguserfieldcddesc', VARCHAR(100), comment='The Organization User Field Code Description is the description of the user field code.'),
    Column('orguserfieldvalue', VARCHAR(254)),
    Column('orguserfieldvaluedesc', VARCHAR(254)),
    Column('orgdatelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when this ORGUSERFIELDS row was most recently updated. SYSTEM  USE  ONLY'),
    Column('rundate', DateTime, comment='The post date when the WH_ORGUSERFIELDS table was populated. SYSTEM  USE  ONLY'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when the WH_ORGUSERFIELDS table was populated. SYSTEM  USE  ONLY'),
    schema='COCCDM'
)


t_wh_pers = Table(
    'wh_pers', Base.metadata,
    Column('persnbr', NUMBER(22, 0, False), comment='The Person Number is the system assigned number that identifies every person.'),
    Column('persname', VARCHAR(60), comment="The Person Name is the person's name, First name, Middle initial and Last Name."),
    Column('perssortname', VARCHAR(60), comment='The Person Sort Name is the Sort Name for the person.'),
    Column('taxid', VARCHAR(60), comment='The Tax Identification Number for this person.'),
    Column('adddate', DateTime, comment='The Add Date is the date the person was added to the system.'),
    Column('datebirth', DateTime, comment='The Date Birth is the birth date for the person.'),
    Column('datedeath', DateTime, comment='The Date Death is the date the person was deceased.'),
    Column('age', NUMBER(4, 0, False), comment='The age of the person when the batch queue is run.'),
    Column('employeeyn', VARCHAR(1), comment='EmployeeYN identifies if the person is an employee of the FI'),
    Column('privacyyn', VARCHAR(1), comment='Privacy YN denotes if the person has allowed information to be released.'),
    Column('cipratingcd', VARCHAR(4), comment='The CIP Rating Code identifies the user defined codes used for person ratings.'),
    Column('naicscd', VARCHAR(6), comment='The NAICS Code is the user assigned code that identifies the North American Industry Classification for a person.'),
    Column('naicsdesc', VARCHAR(254), comment='The description of the NAICS industry type.'),
    Column('siccd', VARCHAR(4), comment='The SIC Code is the user assigned code that identifies the standard industrial class for a person.'),
    Column('sicdesc', VARCHAR(60), comment='The SIC Description is the textual description of the standard industrial class.'),
    Column('sicsubcd', VARCHAR(4), comment='The SICSubCd is a user assigned code that identifies the standard industrial class sub that applies to a person.'),
    Column('sicsubdesc', VARCHAR(60), comment='The SIC Subordinate Description is the textual description of the standard industry class subordinate codes.'),
    Column('creditscore', VARCHAR(15), comment='The numeric value assigned to rate the ability to repay a debit.'),
    Column('spousepersnbr', NUMBER(22, 0, False), comment='The Person Number is the system assigned number that identifies every person.'),
    Column('spousepersname', VARCHAR(60), comment="The Person Name is the person's name, First name, Middle initial and Last Name."),
    Column('spouseperssortname', VARCHAR(60), comment='The Person Sort Name is the Sort Name for the person'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='POSTDATE'),
    Column('rundate', DateTime, comment='SYSDATE'),
    Column('homeemail', VARCHAR(40)),
    Column('busemail', VARCHAR(40)),
    Column('allowpromoyn', VARCHAR(1), comment='Determines if promo calls and messages are allowed.'),
    schema='COCCDM'
)


t_wh_persperstyp = Table(
    'wh_persperstyp', Base.metadata,
    Column('persnbr', NUMBER(22, 0, False), nullable=False),
    Column('perstypcd', VARCHAR(4)),
    Column('rundate', DateTime, nullable=False),
    Column('perstypdesc', VARCHAR(30)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_persuserfields = Table(
    'wh_persuserfields', Base.metadata,
    Column('persnbr', NUMBER(22, 0, False), nullable=False, comment='The Person Number is a system-assigned primary key that uniquely identifies the person. '),
    Column('persuserfieldcd', VARCHAR(4), comment='The Person User Field Code is the user field code associated with the person. '),
    Column('persuserfieldcddesc', VARCHAR(100), comment='The Person User Field Code Description is the description of the user field code.'),
    Column('persuserfieldvalue', VARCHAR(254)),
    Column('persuserfieldvaluedesc', VARCHAR(254)),
    Column('persdatelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when this PERSUSERFIELDS row was most recently updated. SYSTEM  USE  ONLY'),
    Column('rundate', DateTime, comment='The post date when the WH_PERSUSERFIELDS table was populated. SYSTEM  USE  ONLY'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when the WH_PERSUSERFIELDS table was populated. SYSTEM  USE  ONLY'),
    schema='COCCDM'
)


t_wh_phone = Table(
    'wh_phone', Base.metadata,
    Column('persnbr', NUMBER(22, 0, False), nullable=False),
    Column('phoneusecd', VARCHAR(4), nullable=False),
    Column('phoneseq', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('areacd', VARCHAR(3)),
    Column('exchange', VARCHAR(3)),
    Column('phonenbr', VARCHAR(4)),
    Column('phoneexten', VARCHAR(4)),
    Column('foreignphonenbr', VARCHAR(10)),
    Column('ctrycd', VARCHAR(4), nullable=False),
    Column('phoneusedesc', VARCHAR(30)),
    Column('datelastmaint', DateTime, nullable=False),
    Column('preferredyn', VARCHAR(1), comment='Determines the preferred phone number to use.'),
    schema='COCCDM'
)


class WhPreauth(Base):
    __tablename__ = 'wh_preauth'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'balcatcd', 'baltypcd', 'allotnbr', name='pk_wh_preauth'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Account Number is the system assigned number that uniquely identifies each account.')
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, comment='The date of the extract.')
    balcatcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True, comment='The Balance Category Code is the user defined code used to identify the balance categories.')
    baltypcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True, comment='The Balance Type Code is the user defined code used to identify the balance types.')
    allotnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Allotment Number is the system generated number of the allotment.')
    rtxntypcd: Mapped[str] = mapped_column(VARCHAR(4), comment='The Transaction Type Code identifies the type of allotment performed.')
    rtxntypdesc: Mapped[str] = mapped_column(VARCHAR(30), comment='The Transaction Type Description is the textual description of the transaction type code.')
    effdate: Mapped[datetime.datetime] = mapped_column(DateTime, comment='The Effective Date for the allotment.')
    gracedays: Mapped[float] = mapped_column(NUMBER(22, 0, False), server_default=text('0 '), comment='The Grace Days is the the number of days after the due date that the allotment will be made.')
    achorigyn: Mapped[str] = mapped_column(CHAR(1), server_default=text("'N' "), comment='The ACH Orig identifies the ACH origination of the allotment.')
    currrev: Mapped[float] = mapped_column(NUMBER(22, 0, False), server_default=text('0 '), comment='The Current Revision of the allotment.')
    revdatetime: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='The Revision Date Time of the allotment.')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM  USE  ONLY.')
    allottypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The Allotment Type Code identifies the type of allotment used.')
    allottypdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='The Allotment Type Description is the textual description of the allotment.')
    calperiodcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The Calculation Period Code identifies the Calculation Period used.')
    duedaynbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Due Day Number is the due day for the allotment.')
    dueweekdaycd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The Due Week Day Code is the day of the week that the allotment is due.')
    firstmonthcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The First Month Code identifies the first month for the allotment.')
    nextdisbdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The Next Disbursement date for the allotment.')
    enddate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The End Date for the allotment.')
    recvinternlacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Receiving Internal Account Number for the allotment.')
    fixedamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True), comment='The Fixed Dollar Amount for the allotment.')
    excessamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='The Excess Amount for the allotment.')
    memo: Mapped[Optional[str]] = mapped_column(VARCHAR(254), comment='The Memo of the allotment.')
    initialduedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The Initial Due Date of the allotment.')
    nextreqduedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The Next Due Date of the allotment.')
    inactivedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The Inactive Date of the allotment.')
    extacctname: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='The External Account Name of the allotment.')
    recvroutenbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Receiving Route Number of the allotment.')
    extacctnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(22), comment='The External Account Number of the allotment.')
    addldesc: Mapped[Optional[str]] = mapped_column(VARCHAR(80), comment='The Additional Description of the allotment.')
    achrecvaccttypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The ACH Receivable Account Type of the allotment.')
    achrecvacctdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='The ACH Receivable Account Type Description of the allotment.')
    achrecvtypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='ACH Receivable Type Code . The code representing the receiver type code for the ACH allotment.')


t_wh_prop = Table(
    'wh_prop', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False)),
    Column('rundate', DateTime, nullable=False),
    Column('propnbr', NUMBER(22, 0, False), nullable=False),
    Column('proptypecd', VARCHAR(4), nullable=False),
    Column('aprsvalueamt', NUMBER(22, 2, True)),
    Column('aprsdate', DateTime),
    Column('taxtowncd', NUMBER(22, 0, False)),
    Column('taxtown', VARCHAR(40)),
    Column('taxtypecd', VARCHAR(4)),
    Column('taxdisbperiod', VARCHAR(4)),
    Column('taxescrowyn', CHAR(1), server_default=text('null')),
    Column('nbrofunits', NUMBER(22, 0, False)),
    Column('propaddr1', VARCHAR(40)),
    Column('propaddr2', VARCHAR(40)),
    Column('propaddr3', VARCHAR(40)),
    Column('propcity', VARCHAR(40)),
    Column('propstate', VARCHAR(2)),
    Column('propzip', VARCHAR(10)),
    Column('datelastmaint', DateTime, nullable=False),
    Index('wh_prop_dx1', 'acctnbr'),
    schema='COCCDM'
)


t_wh_prop2 = Table(
    'wh_prop2', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False)),
    Column('propnbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('proptypcd', VARCHAR(4), nullable=False),
    Column('acceptdate', DateTime),
    Column('marginpct', NUMBER(8, 7, True)),
    Column('reviewcalperiodcd', VARCHAR(4)),
    Column('lastreviewdate', DateTime),
    Column('effdate', DateTime),
    Column('inactivedate', DateTime),
    Column('proptypdesc', VARCHAR(30)),
    Column('propconditioncd', VARCHAR(4)),
    Column('propconditiondesc', VARCHAR(30)),
    Column('addrnbr', NUMBER(22, 0, False)),
    Column('locdesc', VARCHAR(30)),
    Column('propid', VARCHAR(30)),
    Column('platenbr', VARCHAR(12)),
    Column('platestatecd', VARCHAR(2)),
    Column('propmake', VARCHAR(30)),
    Column('propmodel', VARCHAR(30)),
    Column('fleetnbr', VARCHAR(12)),
    Column('propvalue', NUMBER(22, 0, False)),
    Column('taxvalue', NUMBER(22, 0, False)),
    Column('camaintfee', NUMBER(22, 0, False)),
    Column('casqft', NUMBER(22, 0, False)),
    Column('platbooknbr', VARCHAR(16)),
    Column('platbookpage', VARCHAR(16)),
    Column('lotnbr', VARCHAR(16)),
    Column('propsqft', NUMBER(22, 0, False)),
    Column('propdesc', VARCHAR(254)),
    Column('owndate', DateTime),
    Column('dprmonths', NUMBER(22, 0, False)),
    Column('datelastaudit', DateTime),
    Column('datelastassm', DateTime),
    Column('settlementdate', DateTime),
    Column('settlementprice', NUMBER(asdecimal=False)),
    Column('purchasedate', DateTime),
    Column('purchaseprice', NUMBER(asdecimal=False)),
    Column('floodzoneyn', CHAR(1), nullable=False),
    Column('lastenvauditdate', DateTime),
    Column('residualvalueamt', NUMBER(22, 0, False)),
    Column('certnbr', VARCHAR(20)),
    Column('cusipnbr', VARCHAR(10)),
    Column('cusipsymbol', VARCHAR(6)),
    Column('nbrofunits', NUMBER(22, 0, False)),
    Column('unitvalue', NUMBER(22, 0, False)),
    Column('valuedate', DateTime),
    Column('maturitydate', DateTime),
    Column('sectionnbr', VARCHAR(16)),
    Column('townshipnbr', VARCHAR(16)),
    Column('mapnbr', VARCHAR(16)),
    Column('blocknbr', VARCHAR(16)),
    Column('floodpanel', VARCHAR(30)),
    Column('floodcommunity', NUMBER(22, 0, False)),
    Column('floodzone', VARCHAR(6)),
    Column('redeterminationdate', DateTime),
    Column('builddate', DateTime),
    Column('owneroccupiedcd', VARCHAR(4)),
    Column('owneroccupieddesc', VARCHAR(30)),
    Column('datelastmaint', DateTime, nullable=False),
    Column('propvehicleodometer', NUMBER(22, 0, False)),
    Column('propnewyn', VARCHAR(1), nullable=False),
    Column('propyearnbr', NUMBER(22, 0, False)),
    Column('occupancyeffdate', DateTime, comment='The Effective Date of the owner occupied code for the property; relates to Prop.OwnerOccupCd.'),
    Column('parcelnbr', VARCHAR(50), comment='The parcel number for the prop number.'),
    schema='COCCDM'
)


t_wh_propuserfields = Table(
    'wh_propuserfields', Base.metadata,
    Column('propnbr', NUMBER(22, 0, False), nullable=False, comment='The Property Number is a system-assigned primary key that uniquely identifies the property. '),
    Column('propuserfieldcd', VARCHAR(4), comment='The Property User Field Code is the user field code associated with the property. '),
    Column('propuserfieldcddesc', VARCHAR(100), comment='The Property User Field Code Description is the description of the user field code.'),
    Column('propuserfieldvalue', VARCHAR(254)),
    Column('propuserfieldvaluedesc', VARCHAR(254)),
    Column('propdatelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when this PROPUSERFIELDS row was most recently updated. SYSTEM  USE  ONLY'),
    Column('rundate', DateTime, comment='The post date when the WH_PROPUSERFIELDS table was populated. SYSTEM  USE  ONLY'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when the WH_PROPUSERFIELDS table was populated. SYSTEM  USE  ONLY'),
    schema='COCCDM'
)


t_wh_rtxn = Table(
    'wh_rtxn', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False)),
    Column('rundate', DateTime, nullable=False),
    Column('rtxnnbr', NUMBER(22, 0, False)),
    Column('parentrtxnnbr', NUMBER(22, 0, False)),
    Column('applnbr', NUMBER(22, 0, False)),
    Column('applname', VARCHAR(60)),
    Column('rtxntypcd', VARCHAR(4)),
    Column('rtxntypdesc', VARCHAR(60)),
    Column('holdacctnbr', NUMBER(22, 0, False)),
    Column('currrtxnstatcd', VARCHAR(4)),
    Column('tranamt', NUMBER(22, 2, True)),
    Column('origpostdate', DateTime),
    Column('rtxnreasoncd', VARCHAR(4)),
    Column('actdatetime', DateTime),
    Column('effdate', DateTime),
    Column('origpersnbr', NUMBER(22, 0, False)),
    Column('apprpersnbr', NUMBER(22, 0, False)),
    Column('rtxnstatcd', VARCHAR(4)),
    Column('cashboxnbr', NUMBER(22, 0, False)),
    Column('extrtxndesctext', VARCHAR(128)),
    Column('origntwknodenbr', NUMBER(22, 0, False)),
    Column('orgnbr', NUMBER(22, 0, False)),
    Column('allotnbr', NUMBER(22, 0, False)),
    Column('reversalrtxnnbr', NUMBER(22, 0, False)),
    Column('rtmttxncatcd', VARCHAR(4)),
    Column('rtmtyr', NUMBER(22, 0, False)),
    Column('rtxnsourcecd', VARCHAR(4)),
    Column('intrrtxndesctext', VARCHAR(128)),
    Column('postdate', DateTime),
    Column('checknbr', NUMBER(22, 0, False)),
    Column('agreenbr', NUMBER(22, 0, False)),
    Column('transourcekey', VARCHAR(30)),
    Column('membernbr', NUMBER(22, 0, False)),
    Column('networkcd', VARCHAR(4)),
    Column('cardtxnnbr', NUMBER(22, 0, False)),
    Column('datelastmaint', DateTime),
    Column('payto', VARCHAR(140), comment='The pay to column identifies who the check was made payable.'),
    Column('parentacctnbr', NUMBER(22, 0, False), comment='The Parent Account Number is the related parent account number for an account.'),
    Column('txnfeeamt', NUMBER(22, 2, True), comment='The Fee Amount for the transaction.'),
    Column('otcpersnbr', NUMBER(22, 0, False), comment='Person number is a unique identifier assigned to a person entity in the database.  This attribute indicates the person who transacted business that resulted in the transaction.'),
    Column('sourceid', VARCHAR(20), comment='Identifies the source of the file.'),
    Column('companyentrydesc', VARCHAR(10), comment='Filerecord description for the entry.'),
    Index('wh_rtxn_dx1', 'acctnbr', 'rtxnnbr'),
    schema='COCCDM'
)


t_wh_rtxn_temp = Table(
    'wh_rtxn_temp', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False)),
    Column('rundate', DateTime),
    Column('rtxnnbr', NUMBER(22, 0, False)),
    Column('parentrtxnnbr', NUMBER(22, 0, False)),
    Column('applnbr', NUMBER(22, 0, False)),
    Column('applname', VARCHAR(60)),
    Column('rtxntypcd', VARCHAR(4)),
    Column('rtxntypdesc', VARCHAR(60)),
    Column('holdacctnbr', NUMBER(22, 0, False)),
    Column('currrtxnstatcd', VARCHAR(4)),
    Column('tranamt', NUMBER(22, 2, True)),
    Column('origpostdate', DateTime),
    Column('rtxnreasoncd', VARCHAR(4)),
    Column('actdatetime', DateTime),
    Column('effdate', DateTime),
    Column('origpersnbr', NUMBER(22, 0, False)),
    Column('apprpersnbr', NUMBER(22, 0, False)),
    Column('rtxnstatcd', VARCHAR(4)),
    Column('cashboxnbr', NUMBER(22, 0, False)),
    Column('extrtxndesctext', VARCHAR(128)),
    Column('origntwknodenbr', NUMBER(22, 0, False)),
    Column('orgnbr', NUMBER(22, 0, False)),
    Column('allotnbr', NUMBER(22, 0, False)),
    Column('reversalrtxnnbr', NUMBER(22, 0, False)),
    Column('rtmttxncatcd', VARCHAR(4)),
    Column('rtmtyr', NUMBER(22, 0, False)),
    Column('rtxnsourcecd', VARCHAR(4)),
    Column('intrrtxndesctext', VARCHAR(128)),
    Column('postdate', DateTime),
    Column('checknbr', NUMBER(22, 0, False)),
    Column('agreenbr', NUMBER(22, 0, False)),
    Column('transourcekey', VARCHAR(30)),
    Column('membernbr', NUMBER(22, 0, False)),
    Column('networkcd', VARCHAR(4)),
    Column('cardtxnnbr', NUMBER(22, 0, False)),
    Column('datelastmaint', DateTime),
    Column('payto', VARCHAR(140), comment='The pay to column identifies who the check was made payable.'),
    Column('parentacctnbr', NUMBER(22, 0, False), comment='The Parent Account Number is the related parent account number for an account.'),
    Column('txnfeeamt', NUMBER(22, 2, True), comment='The Fee Amount for the transaction.'),
    Column('otcpersnbr', NUMBER(22, 0, False), comment='Person number is a unique identifier assigned to a person entity in the database.  This attribute indicates the person who transacted business that resulted in the transaction.'),
    Column('sourceid', VARCHAR(20), comment='Identifies the source of the file.'),
    Column('companyentrydesc', VARCHAR(10), comment='Filerecord description for the entry.'),
    Index('wh_rtxn_temp_dx1', 'acctnbr', 'rtxnnbr'),
    schema='COCCDM'
)


t_wh_rtxnbal = Table(
    'wh_rtxnbal', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False)),
    Column('rundate', DateTime),
    Column('rtxnnbr', NUMBER(22, 0, False)),
    Column('rtxntypcd', VARCHAR(4)),
    Column('rtxntypdesc', VARCHAR(30)),
    Column('subacctnbr', NUMBER(22, 0, False)),
    Column('balcatcd', VARCHAR(4)),
    Column('baltypcd', VARCHAR(4)),
    Column('balancedesc', VARCHAR(70)),
    Column('amt', NUMBER(15, 2, True)),
    Column('datelastmaint', DateTime),
    Index('wh_rtxnbal_dx1', 'acctnbr', 'rtxnnbr'),
    schema='COCCDM'
)


t_wh_rtxnbal_temp = Table(
    'wh_rtxnbal_temp', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False)),
    Column('rundate', DateTime),
    Column('rtxnnbr', NUMBER(22, 0, False)),
    Column('rtxntypcd', VARCHAR(4)),
    Column('rtxntypdesc', VARCHAR(30)),
    Column('subacctnbr', NUMBER(22, 0, False)),
    Column('balcatcd', VARCHAR(4)),
    Column('baltypcd', VARCHAR(4)),
    Column('balancedesc', VARCHAR(70)),
    Column('amt', NUMBER(15, 2, True)),
    Column('datelastmaint', DateTime),
    Index('wh_rtxnbal_temp_dx1', 'acctnbr', 'rtxnnbr'),
    schema='COCCDM'
)


class WhRtxncard(Base):
    __tablename__ = 'wh_rtxncard'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rtxnnbr', name='pk_wh_rtxncard'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Account Number is the system assigned number that uniquely identifies each account.')
    rtxnnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Transaction Number is the system assigned number used to identify each transaction.')
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, comment='The date of the extract.')
    cardtxnnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), comment='The Card Transaction Number is the system assigned number used to identify each card transaction.')
    atmswitchcd: Mapped[str] = mapped_column(VARCHAR(4), server_default=text("'PRI' "), comment='A code recieved from a ATM Switch with which the Financial Institution has agreements.')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM  USE  ONLY.')
    rtxntypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The Transaction Type Code is a user assigned code that identifies the valid transactions.')
    agreenbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Agree Number is the system assigned number used to identify each agreement.')
    cardnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(24), comment='The Card Number is the system assigned number used to identify each card.')
    cardholder: Mapped[Optional[str]] = mapped_column(VARCHAR(50), comment='The CardHolder is the name of the card holder.')
    processtypcd: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Process Type Code is the code of process type.')
    processtypdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='The Process Type Description is the description of process type.')
    responsecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The Response Code is the response code for card transaction.')
    responsedesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='The Response Description is the response description for card transaction.')
    reversalreasoncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The Reversal Reason Code is the reversal reason code for card transaction.')
    reversalreasondesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='The Reversal Reason Description is the reversal reason description for card transaction.')
    advicereasoncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The Advice Reason Code is the advice reason code for card transaction.')
    advicereasondesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='The Advice Reason Description is the advice reason description for card transaction.')
    membernbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Member Number is the used to identify each member number.')
    isotxncd: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Iso Transaction Code is the iso transaction code for card transaction.')
    isotxndesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='The Iso Transaction Description is the iso transaction description for card transaction.')
    txnamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True), comment='The Transaction Amount is the transaction amount for card transaction.')
    authamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True), comment='The Authorized Amount is the authorized amount for card transaction.')
    txnfeeamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True), comment='The Transaction Fee Amount is the transaction fee amount for card transaction.')
    storeforwardyn: Mapped[Optional[str]] = mapped_column(CHAR(1), comment='The Store Forward is used to identify store forward for card transaction.')
    fromacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Identifies From Account Number.')
    fromaccttypcd: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Identifies From Account Type Code.')
    fromaccttypdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='Identifies From Account Type Description.')
    fromextrtxndesctext: Mapped[Optional[str]] = mapped_column(VARCHAR(128), comment='The External Transaction Description Text is the texual description of the from account.')
    toacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Identifies To Account Number.')
    toaccttypcd: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Identifies To Account Type Code.')
    toaccttypdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='Identifies To Account Type Description.')
    toextrtxndesctext: Mapped[Optional[str]] = mapped_column(VARCHAR(128), comment='The External Transaction Description Text is the texual description of the to account.')
    holdamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True), comment='The hold amount establishes the dollar amount of the hold.')
    holdeffdatetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The effective date and time establishes the point in time that the hold begins.')
    holdinactivedatetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The inactive date and time indicates the point in time that the hold should expire.')
    holddescription: Mapped[Optional[str]] = mapped_column(VARCHAR(128), comment='Identifies Hold Description.')
    settledate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='Identifies Settle Date.')
    activitydate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='Contains the calendar date on which a transaction was handled by the settlement process.')
    termseqnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Identifies Term Sequence Number.')
    traceauditnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Identifies Trace Audit Number.')
    retrefnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(12), comment='The Retrieval Reference Number is a unique number assigned by the message initiator.')
    networkid: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies Network Id.')
    networkdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='Identifies Network Description.')
    acquireinstid: Mapped[Optional[str]] = mapped_column(VARCHAR(11), comment='Identifies Acquire Institution Id.')
    terminalid: Mapped[Optional[str]] = mapped_column(VARCHAR(16), comment='Identifies Terminal Id.')
    mccnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The SIC Subordinate Code is a user assigned code that identifies the valid standard industry class subordinates.')


class WhRtxncardTemp(Base):
    __tablename__ = 'wh_rtxncard_temp'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'rtxnnbr', name='pk_wh_rtxncard_temp'),
        {'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Account Number is the system assigned number that uniquely identifies each account.')
    rtxnnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Transaction Number is the system assigned number used to identify each transaction.')
    rundate: Mapped[datetime.datetime] = mapped_column(DateTime, comment='The date of the extract.')
    cardtxnnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), comment='The Card Transaction Number is the system assigned number used to identify each card transaction.')
    storeforwardyn: Mapped[str] = mapped_column(CHAR(1), server_default=text("'N' "), comment='The Store Forward is used to identify store forward for card transaction.')
    atmswitchcd: Mapped[str] = mapped_column(VARCHAR(4), server_default=text("'PRI' "), comment='A code recieved from a ATM Switch with which the Financial Institution has agreements.')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM  USE  ONLY.')
    rtxntypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The Transaction Type Code is a user assigned code that identifies the valid transactions.')
    agreenbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Agree Number is the system assigned number used to identify each agreement.')
    cardnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(24), comment='The Card Number is the system assigned number used to identify each card.')
    cardholder: Mapped[Optional[str]] = mapped_column(VARCHAR(50), comment='The CardHolder is the name of the card holder.')
    processtypcd: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Process Type Code is the code of process type.')
    processtypdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='The Process Type Description is the description of process type.')
    responsecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The Response Code is the response code for card transaction.')
    responsedesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='The Response Description is the response description for card transaction.')
    reversalreasoncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The Reversal Reason Code is the reversal reason code for card transaction.')
    reversalreasondesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='The Reversal Reason Description is the reversal reason description for card transaction.')
    advicereasoncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The Advice Reason Code is the advice reason code for card transaction.')
    advicereasondesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='The Advice Reason Description is the advice reason description for card transaction.')
    membernbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Member Number is the used to identify each member number.')
    isotxncd: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Iso Transaction Code is the iso transaction code for card transaction.')
    isotxndesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='The Iso Transaction Description is the iso transaction description for card transaction.')
    txnamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True), comment='The Transaction Amount is the transaction amount for card transaction.')
    authamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True), comment='The Authorized Amount is the authorized amount for card transaction.')
    txnfeeamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 2, True), comment='The Transaction Fee Amount is the transaction fee amount for card transaction.')
    fromacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Identifies From Account Number.')
    fromaccttypcd: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Identifies From Account Type Code.')
    fromaccttypdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='Identifies From Account Type Description.')
    fromextrtxndesctext: Mapped[Optional[str]] = mapped_column(VARCHAR(128), comment='The External Transaction Description Text is the texual description of the from account.')
    toacctnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Identifies To Account Number.')
    toaccttypcd: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Identifies To Account Type Code.')
    toaccttypdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='Identifies To Account Type Description.')
    toextrtxndesctext: Mapped[Optional[str]] = mapped_column(VARCHAR(128), comment='The External Transaction Description Text is the texual description of the to account.')
    holdamt: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(22, 3, True), comment='The hold amount establishes the dollar amount of the hold.')
    holdeffdatetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The effective date and time establishes the point in time that the hold begins.')
    holdinactivedatetime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='The inactive date and time indicates the point in time that the hold should expire.')
    holddescription: Mapped[Optional[str]] = mapped_column(VARCHAR(128), comment='Identifies Hold Description.')
    settledate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='Identifies Settle Date.')
    activitydate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='Contains the calendar date on which a transaction was handled by the settlement process.')
    termseqnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Identifies Term Sequence Number.')
    traceauditnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='Identifies Trace Audit Number.')
    retrefnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(12), comment='The Retrieval Reference Number is a unique number assigned by the message initiator.')
    networkid: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='Identifies Network Id.')
    networkdesc: Mapped[Optional[str]] = mapped_column(VARCHAR(30), comment='Identifies Network Description.')
    acquireinstid: Mapped[Optional[str]] = mapped_column(VARCHAR(11), comment='Identifies Acquire Institution Id.')
    terminalid: Mapped[Optional[str]] = mapped_column(VARCHAR(16), comment='Identifies Terminal Id.')
    mccnbr: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The SIC Subordinate Code is a user assigned code that identifies the valid standard industry class subordinates.')


t_wh_rtxnexcphist = Table(
    'wh_rtxnexcphist', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False)),
    Column('rundate', DateTime),
    Column('rtxnnbr', NUMBER(22, 0, False)),
    Column('rtxnexcpnbr', NUMBER(22, 0, False)),
    Column('rtxnexcpdesc', VARCHAR(60)),
    Column('onlineoverrideyn', VARCHAR(1)),
    Column('apprauthcd', VARCHAR(4)),
    Column('authdesc', VARCHAR(30)),
    Column('datelastmaint', DateTime),
    Index('wh_rtxnexcphist_dx1', 'acctnbr', 'rtxnnbr'),
    schema='COCCDM'
)


t_wh_rtxnexcphist_temp = Table(
    'wh_rtxnexcphist_temp', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False)),
    Column('rundate', DateTime),
    Column('rtxnnbr', NUMBER(22, 0, False)),
    Column('rtxnexcpnbr', NUMBER(22, 0, False)),
    Column('rtxnexcpdesc', VARCHAR(60)),
    Column('onlineoverrideyn', VARCHAR(1)),
    Column('apprauthcd', VARCHAR(4)),
    Column('authdesc', VARCHAR(30)),
    Column('datelastmaint', DateTime),
    Index('wh_rtxnexcphist_temp_dx1', 'acctnbr', 'rtxnnbr'),
    schema='COCCDM'
)


t_wh_rtxnfundtyp = Table(
    'wh_rtxnfundtyp', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False, comment='The Account Number is a system-assigned primary key that uniquely identifies each account. '),
    Column('rtxnnbr', NUMBER(22, 0, False), nullable=False, comment='The Transaction Number is the system assigned number that uniquely identifies each transaction. '),
    Column('fundtypcd', VARCHAR(4), nullable=False, comment='The Fund Type Code is the user defined code that identifies the funds type used.'),
    Column('fundtypcddesc', VARCHAR(30), nullable=False, comment='The Fund Type Code Description '),
    Column('fundtypdtlcd', VARCHAR(4), nullable=False, comment='The Fund Type Detail Code is the user defined code that identifies the detail of the funds in a transaction.'),
    Column('fundtypdtldesc', VARCHAR(30), nullable=False),
    Column('clearcatcd', VARCHAR(4), nullable=False, comment='The Clear Category Code is the user defined code that identifies the clear category for the funds in a transaction.'),
    Column('clearcatcddesc', VARCHAR(30), nullable=False, comment='The Clear Category Code Description. '),
    Column('seqnbr', NUMBER(22, 0, False), nullable=False, comment='The Sequence Number is a system assigned number that identifies the sequence of a transaction.'),
    Column('nbrofitems', NUMBER(22, 0, False), comment='The Number of Items is the user assigned number that identifies the number of items in a transaction.'),
    Column('amt', NUMBER(22, 3, True), nullable=False, comment='The Amount identifies the dollar amount of a transaction.'),
    Column('rundate', DateTime, nullable=False, comment='The date that the report is run.'),
    Column('actdatetime', DateTime, nullable=False, comment='The Activity date is the date that the transaction occured.'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM  USE  ONLY'),
    schema='COCCDM'
)


t_wh_rtxnfundtyp_temp = Table(
    'wh_rtxnfundtyp_temp', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False, comment='The Account Number is a system-assigned primary key that uniquely identifies each account. '),
    Column('rtxnnbr', NUMBER(22, 0, False), nullable=False, comment='The Transaction Number is the system assigned number that uniquely identifies each transaction. '),
    Column('fundtypcd', VARCHAR(4), nullable=False, comment='The Fund Type Code is the user defined code that identifies the funds type used.'),
    Column('fundtypcddesc', VARCHAR(30), nullable=False, comment='The Fund Type Code Description '),
    Column('fundtypdtlcd', VARCHAR(4), nullable=False, comment='The Fund Type Detail Code is the user defined code that identifies the detail of the funds in a transaction.'),
    Column('fundtypdtldesc', VARCHAR(30), nullable=False),
    Column('clearcatcd', VARCHAR(4), nullable=False, comment='The Clear Category Code is the user defined code that identifies the clear category for the funds in a transaction.'),
    Column('clearcatcddesc', VARCHAR(30), nullable=False, comment='The Clear Category Code Description. '),
    Column('seqnbr', NUMBER(22, 0, False), nullable=False, comment='The Sequence Number is a system assigned number that identifies the sequence of a transaction.'),
    Column('nbrofitems', NUMBER(22, 0, False), comment='The Number of Items is the user assigned number that identifies the number of items in a transaction.'),
    Column('amt', NUMBER(22, 3, True), nullable=False, comment='The Amount identifies the dollar amount of a transaction.'),
    Column('rundate', DateTime, nullable=False, comment='The date that the report is run.'),
    Column('actdatetime', DateTime, nullable=False, comment='The Activity date is the date that the transaction occured.'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date when this row was most recently updated. SYSTEM  USE  ONLY'),
    schema='COCCDM'
)


class WhSalesReferrals(Base):
    __tablename__ = 'wh_sales_referrals'
    __table_args__ = (
        PrimaryKeyConstraint('referralnbr', 'referralprodnbr', name='pk_wh_sales_referrals'),
        {'schema': 'COCCDM'}
    )

    referralnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Referral Number is the system assigned number that identifies every referral.')
    refpersnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), comment='The RefPersNbr is the number of the person for this referral.')
    referring_emp: Mapped[str] = mapped_column(VARCHAR(65), comment='The Referring_Emp is the full name of the RefPersNbr.')
    createdate: Mapped[datetime.datetime] = mapped_column(DateTime, comment='The CreateDate is the date when this referral is created.')
    duedate: Mapped[datetime.datetime] = mapped_column(DateTime, comment='The DueDate is the date when this referral is due.')
    refteamnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), comment='The RefTeamNbr is the number of the team assigned to this referral.')
    referring_team: Mapped[str] = mapped_column(VARCHAR(255), comment='The Referring_Team is the team name of the RefTeamNbr.')
    referralprodnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The ReferralProdNbr is the product number of the product for use.')
    currrefstatcd: Mapped[str] = mapped_column(VARCHAR(4), comment='The CurrRefStatCd identifies the current referral status code this referral belongs to.')
    status: Mapped[str] = mapped_column(VARCHAR(255), comment='The Status is the description of the CurrRefStatCd.')
    openyn: Mapped[str] = mapped_column(VARCHAR(1), comment='The OpenYN identifies whether the referral is open or not.')
    successfulyn: Mapped[str] = mapped_column(VARCHAR(1), comment='The SuccessfulYN identifies whether the referral is successful or not.')
    customernbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The Customer Number is the number of the customer for use.')
    customer: Mapped[Optional[str]] = mapped_column(VARCHAR(65), comment='The Customer is the full name of the customer.')
    orgcustomernbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The OrgCustomerNbr is the system assigned number used to identify each organization.')
    customer_org: Mapped[Optional[str]] = mapped_column(VARCHAR(60), comment='The Organization Name is the legal name for the organization.')
    assignedpersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The AssignedPersNbr is the number of the person assigned to this referral.')
    assigned: Mapped[Optional[str]] = mapped_column(VARCHAR(65), comment='The Assigned is the full name of the AssignedPersNbr.')
    assignedgrpnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The AssignedGrpNbr is the number of the group assigned to this referral.')
    assigned_grp: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='The Assigned_Grp is the description of the AssignedGrpNbr.')
    contactphonecd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The ContactPhoneCd is the phone use code of this referal.')
    contactaddrnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The ContactAddrNbr is the address number of the address for use.')
    mjaccttypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The MjAcctTypCd identifies which Major Account Type this referral belongs to.')
    miaccttypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The MiAcctTypCd identifies which Minor Account Type this referral belongs to.')
    product: Mapped[Optional[str]] = mapped_column(VARCHAR(9), comment='The Product identifies which Major/Minor Account Type this referral belongs to.')
    agreetypcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The AgreeTypCd identifies which agreement type this referral belongs to.')
    userfieldcd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The UserFieldCd identifies which user field this referral belongs to.')
    userfield: Mapped[Optional[str]] = mapped_column(VARCHAR(100), comment='The UserField is the description of the UserFieldCd.')
    closedbypersnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The ClosedByPersNbr identifies the person who closed this referral.')
    closed_by: Mapped[Optional[str]] = mapped_column(VARCHAR(65), comment='The Closed_By is the full name of the ClosedByPersNbr.')
    closeteamnbr: Mapped[Optional[float]] = mapped_column(NUMBER(22, 0, False), comment='The CloseTeamNbr identifies the team who closed this referral.')
    closed_by_team: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='The Closed_By_Team is the team name of the CloseTeamNbr.')
    closereasoncd: Mapped[Optional[str]] = mapped_column(VARCHAR(4), comment='The CloseReasonCd identifies the reason of this referral closing.')
    closereasondesc: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='The CloseReasonDesc is the description of the CloseReasonCd.')


class WhSalesReferraluserfield(Base):
    __tablename__ = 'wh_sales_referraluserfield'
    __table_args__ = (
        PrimaryKeyConstraint('referralnbr', 'userfieldcd', name='pk_wh_sales_referraluserfield'),
        {'schema': 'COCCDM'}
    )

    referralnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='The Referral Number is the system assigned number that identifies every referral.')
    userfieldcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True, comment='The UserFieldCd identifies which user field this referral belongs to.')
    userfield: Mapped[Optional[str]] = mapped_column(VARCHAR(100), comment='The UserField is the description of the UserFieldCd.')
    value: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='The Value is the value assigned to UserFieldCd of the referral.')


t_wh_sdbacct = Table(
    'wh_sdbacct', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False),
    Column('sdbboxnbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('sdbboxname', VARCHAR(254)),
    Column('sdbnestnbr', NUMBER(22, 0, False), nullable=False),
    Column('nextduedate', DateTime),
    Column('billcalperiodcd', VARCHAR(4), nullable=False),
    Column('branchbankorgnbr', NUMBER(22, 0, False), nullable=False),
    Column('sdbnestname', VARCHAR(254)),
    Column('sdbnestprefix', VARCHAR(10)),
    Column('sdbtypdesc', VARCHAR(254)),
    Column('sdbboxsizehwd', VARCHAR(50)),
    Column('sdbsectnbr', NUMBER(22, 0, False)),
    Column('sdbsectname', VARCHAR(254)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_sdbactivity = Table(
    'wh_sdbactivity', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False)),
    Column('sdbboxnbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('sdbboxname', VARCHAR(254)),
    Column('actvpersnbr', NUMBER(22, 0, False), nullable=False),
    Column('resppersnbr', NUMBER(22, 0, False), nullable=False),
    Column('sdbactvtime', DateTime),
    Column('sdbefftime', DateTime),
    Column('sdbnestnbr', NUMBER(22, 0, False), nullable=False),
    Column('sdbnestprefix', VARCHAR(10)),
    Column('sdbactvtypdesc', VARCHAR(254)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_sdbfee = Table(
    'wh_sdbfee', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False)),
    Column('rundate', DateTime),
    Column('sdbtypdesc', VARCHAR(254)),
    Column('sdbtypannfeetypfeeamt', NUMBER(15, 2, True)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_sdbinvlist = Table(
    'wh_sdbinvlist', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False),
    Column('sdbboxinvlistnbr', NUMBER(22, 0, False), nullable=False),
    Column('sdbboxinvlistentrynbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('locorgnbr', NUMBER(22, 0, False), nullable=False),
    Column('sdbboxinvlistcontainer', VARCHAR(254)),
    Column('sdbboxinvlistentrytext', VARCHAR(2000)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_sdbwaitlist = Table(
    'wh_sdbwaitlist', Base.metadata,
    Column('branchorgnbr', NUMBER(22, 0, False), nullable=False),
    Column('sdbwaitnbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('persnbr', NUMBER(22, 0, False), nullable=False),
    Column('sdbwaitadddate', DateTime),
    Column('sdbwaitstatdesc', VARCHAR(254)),
    Column('sdbwaitnotetext', VARCHAR(2000)),
    Column('sdbwaitnotifydate', DateTime),
    Column('sdbtypdesc', VARCHAR(254)),
    Column('datelastmaint', DateTime, nullable=False),
    schema='COCCDM'
)


t_wh_sic = Table(
    'wh_sic', Base.metadata,
    Column('orgnbr', NUMBER(22, 0, False)),
    Column('siccd', VARCHAR(4)),
    Column('sicsubcd', VARCHAR(4)),
    Column('rundate', DateTime),
    Column('sicdesc', VARCHAR(60)),
    Column('sicsubdesc', VARCHAR(60)),
    Column('datelastmaint', DateTime, nullable=False),
    Column('persnbr', NUMBER(22, 0, False), comment='The person number is the system assigned number that uniquely indentifies each person.'),
    Column('naicsnbr', NUMBER(22, 0, False), comment='The naicsnbr is the user assigned code that identifies the north American industry classification for a person.'),
    Column('naicstypcd', VARCHAR(4), comment='The naics type code is the code used to identify the hierarchical industry group in which each naicscd resides.'),
    Column('naicscd', VARCHAR(6), comment='The government assigned naics industry class code.'),
    Column('naicsdesc', VARCHAR(254), comment='The government assigned naics industry description.'),
    schema='COCCDM'
)


t_wh_sweep = Table(
    'wh_sweep', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), comment='The acctnbr column is the sweep account for which associated min; maxbalgoals apply.'),
    Column('rundate', DateTime, comment='Queue Effective Date'),
    Column('parentacctnbr', NUMBER(22, 0, False), comment='The parentacctnbr is the parent account which will be used when sweeping to; from.'),
    Column('minbalgoal', NUMBER(15, 2, True), comment='The minbalgoal column is the minimum balance, below which funds will be pulled from the parentacctnbr.'),
    Column('maxbalgoal', NUMBER(15, 2, True), comment='The maxbalgoal column is the maximum balance, above which funds will be pushed to the parentacctnbr.'),
    Column('sweepseqnbr', NUMBER(22, 0, False), comment='The currlevelsweepseqnbr column specifies the order in which child accounts will be investigated when sweeping to;from the same parentacctnbr.'),
    Column('minsweepincr', NUMBER(15, 2, True), comment='The minsweepincr column is the minimum incremental amount by which funds are swept within the sweep group.'),
    Column('midpointbalgoal', NUMBER(15, 2, True), comment='The midpointbalgoal column identifies what, if any, midpoint balance should be achieved when the sweeping of funds is required.'),
    Column('datelastmaint', DateTime, nullable=False, server_default=text('SYSDATE '), comment='The date last maintenance is the date when this row was most recently updated. System use only.'),
    Column('investacctnbr', NUMBER(22, 0, False), comment='The InvestAcctNbr column is  the related investment account to which excess funds will be pushed.'),
    Column('loanacctnbr', NUMBER(22, 0, False), comment='The LoanAcctNbr column is the related loan account from which a shortage of funds will be pulled.'),
    Column('sweepmastertranmethcd', VARCHAR(4), comment='The SweepMasterTranMethCd column is the method which identifies the order in which investment and loan accounts should be satisfied.'),
    Column('sweepmastertranmethdesc', VARCHAR(30), comment='The SweepMasterTranMethDesc column describes the associated master transfer method.'),
    Column('sweepavailmethcd', VARCHAR(4), comment='The SweepAvailMethCd column is the availability method used when determining sweep min;max goals (ie. actual, collected, etc)'),
    Column('availmethdesc', VARCHAR(30), comment='The AvailMethDesc column describes the method by which funds availability is determined.'),
    Column('autosweepyn', VARCHAR(1), comment='Trigger Sweep function automatically based on threshold balances.'),
    Column('suspuntildate', DateTime, comment='The date that auto sweep flag should change to Y after it was suspended for buy/sell transaction. Based on FI defined number of days.'),
    schema='COCCDM'
)


t_wh_tax = Table(
    'wh_tax', Base.metadata,
    Column('acctnbr', NUMBER(22, 0, False), nullable=False),
    Column('rundate', DateTime, nullable=False),
    Column('propnbr', NUMBER(22, 0, False)),
    Column('taxorgnbr', NUMBER(22, 0, False), nullable=False),
    Column('taxtypcd', VARCHAR(4), nullable=False),
    Column('calperiodcd', VARCHAR(4)),
    Column('firstmonthcd', VARCHAR(4)),
    Column('duedaynbr', NUMBER(22, 0, False)),
    Column('dueweekdaycd', VARCHAR(4)),
    Column('taxamt', NUMBER(15, 2, True)),
    Column('effdate', DateTime),
    Column('inactivedate', DateTime),
    Column('escrowyn', CHAR(1), nullable=False),
    Column('firstyearnbr', NUMBER(22, 0, False)),
    Column('extpropid', VARCHAR(40)),
    Column('exttracenbr', VARCHAR(40)),
    Column('detailseqnbr', NUMBER(22, 0, False)),
    Column('detailmonthcd', VARCHAR(4)),
    Column('detailduedaynbr', NUMBER(22, 0, False)),
    Column('detailtaxamt', NUMBER(15, 2, True)),
    Column('taxtypdesc', VARCHAR(30)),
    Column('datelastmaint', DateTime, nullable=False),
    Column('taxtown', VARCHAR(60)),
    schema='COCCDM'
)


class WhTotalpaymentsdue(Base):
    __tablename__ = 'wh_totalpaymentsdue'
    __table_args__ = (
        PrimaryKeyConstraint('acctnbr', 'duedate', name='pk_wh_totalpaymentsdue'),
        {'comment': 'TOTALPAYMENTSDUE table is a breakdown of Total Payments Due',
     'schema': 'COCCDM'}
    )

    acctnbr: Mapped[float] = mapped_column(NUMBER(22, 0, False), primary_key=True, comment='This column discloses the account number.')
    duedate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True, comment='This column discloses the date the amount(receivable) is due')
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('SYSDATE '), comment='This column discloses the date that the report was populated.')
    principaldue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='This column discloses the amount of principal that is due within the receivable')
    interestdue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='This column discloses the amount of interest that is due within the receivable')
    escrowdue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='This column discloses the amount of escrow that is due within the receivable')
    latechargedue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='This column discloses the amount of late charges that is due within the receivable')
    notedue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='This column discloses the total amount of the payment for loans that have a FDUE type of loan payment')
    miscdue: Mapped[Optional[decimal.Decimal]] = mapped_column(NUMBER(15, 2, True), comment='This column discloses the amount of miscellaneous amounts due within this receivable.')
    rundate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='This column discloses the postdate of the database.')


class Wrnflag(Base):
    __tablename__ = 'wrnflag'
    __table_args__ = (
        PrimaryKeyConstraint('wrnflagcd', name='pk_wrnflag'),
        {'schema': 'COCCDM'}
    )

    wrnflagcd: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True)
    wrnflagdesc: Mapped[str] = mapped_column(VARCHAR(30))
    datelastmaint: Mapped[datetime.datetime] = mapped_column(DateTime)
    notificationyn: Mapped[str] = mapped_column(CHAR(1))
    acctflagyn: Mapped[str] = mapped_column(CHAR(1))
    persflagyn: Mapped[str] = mapped_column(CHAR(1))


t_xfr_account = Table(
    'xfr_account', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('type', VARCHAR(20)),
    schema='COCCDM'
)


t_xfr_achaccount = Table(
    'xfr_achaccount', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('userid', VARCHAR(32)),
    Column('institutionname', VARCHAR(36)),
    Column('routingnumber', VARCHAR(9)),
    Column('accountnumber', VARCHAR(24)),
    Column('accounttype', VARCHAR(20)),
    Column('creationdatetimeutc', DateTime, nullable=False),
    Column('nickname', VARCHAR(120)),
    Column('deleted', VARCHAR(5)),
    Column('operationsxml', Text),
    Column('reset', VARCHAR(5)),
    schema='COCCDM'
)


t_xfr_achbatch = Table(
    'xfr_achbatch', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('creationdatetimeutc', DateTime, nullable=False),
    Column('effectiveentrydate', DateTime, nullable=False),
    Column('status', VARCHAR(20)),
    Column('statusdatetimeutc', DateTime, nullable=False),
    Column('outfiledownloaddatetimeutc', DateTime),
    Column('infiledownloaddatetimeutc', DateTime),
    Column('rundate', DateTime, nullable=False),
    Column('reversaloutfiledownloaddateutc', DateTime),
    Column('reversalinfiledownloaddateutc', DateTime),
    Column('uninitiatedatetimeutc', DateTime),
    Column('deleted', VARCHAR(5)),
    schema='COCCDM'
)


t_xfr_achtransaction = Table(
    'xfr_achtransaction', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('achbatchid', NUMBER(19, 0, False)),
    Column('status', VARCHAR(20)),
    Column('failurereason', VARCHAR(120)),
    Column('operationsxml', Text),
    Column('constraintssatisfied', VARCHAR(5)),
    schema='COCCDM'
)


t_xfr_achtransfer = Table(
    'xfr_achtransfer', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('individualname', VARCHAR(22)),
    Column('achbatchid', NUMBER(19, 0, False)),
    Column('riskscore', NUMBER(10, 0, False), nullable=False),
    Column('cancellationreason', VARCHAR(120)),
    Column('achtransactiontype', VARCHAR(20)),
    Column('externalachaccountid', NUMBER(19, 0, False), nullable=False),
    Column('internalhostaccountid', NUMBER(19, 0, False)),
    Column('institutionuserid', VARCHAR(32)),
    Column('externalinstitutionname', VARCHAR(36)),
    Column('externalroutingnumber', VARCHAR(9)),
    Column('externalachaccountnumber', VARCHAR(24)),
    Column('externalachaccounttype', VARCHAR(20)),
    Column('internalaccountnumber', VARCHAR(40)),
    Column('internalachaccountnumber', VARCHAR(24)),
    Column('internalachaccounttype', VARCHAR(20)),
    Column('recurring', VARCHAR(5)),
    schema='COCCDM'
)


t_xfr_hostaccount = Table(
    'xfr_hostaccount', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('hostaccountid', VARCHAR(64)),
    Column('achaccountnumber', VARCHAR(24)),
    Column('achaccounttype', VARCHAR(20)),
    Column('regdlimited', VARCHAR(5)),
    Column('accountnumber', VARCHAR(40)),
    schema='COCCDM'
)


t_xfr_hosttransfertransaction = Table(
    'xfr_hosttransfertransaction', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('hosttransactionid', VARCHAR(20)),
    Column('executiondatetimeutc', DateTime, nullable=False),
    Column('succeeded', VARCHAR(5)),
    Column('failurereason', VARCHAR(1000)),
    schema='COCCDM'
)


t_xfr_scheduledtransfer = Table(
    'xfr_scheduledtransfer', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('type', VARCHAR(20)),
    Column('dataspace', VARCHAR(10)),
    Column('userid', VARCHAR(32)),
    Column('sourceaccountid', NUMBER(19, 0, False), nullable=False),
    Column('destinationaccountid', NUMBER(19, 0, False), nullable=False),
    Column('paymenttype', VARCHAR(20)),
    Column('amount', NUMBER(19, 4, True), nullable=False),
    Column('schedulexml', Text),
    Column('leadtime', NUMBER(3, 0, False), nullable=False),
    Column('description', VARCHAR(120)),
    Column('sendsuccessnotification', VARCHAR(5)),
    Column('currentruncount', NUMBER(5, 0, False), nullable=False),
    Column('previousrundate', DateTime),
    Column('nextrundate', DateTime),
    Column('deleted', VARCHAR(5)),
    Column('creationdatetime', DateTime, nullable=False),
    Column('creationdatetimeutc', DateTime, nullable=False),
    Column('submittedbyuserid', VARCHAR(32)),
    Column('contributionyear', VARCHAR(20)),
    Column('status', VARCHAR(20)),
    Column('approvalsrequired', NUMBER(3, 0, False)),
    Column('actionsxml', Text),
    schema='COCCDM'
)


t_xfr_transaction = Table(
    'xfr_transaction', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('type', VARCHAR(20)),
    Column('parenttransferid', NUMBER(19, 0, False), nullable=False),
    schema='COCCDM'
)


t_xfr_transfer = Table(
    'xfr_transfer', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('type', VARCHAR(20)),
    Column('dataspace', VARCHAR(10)),
    Column('userid', VARCHAR(32)),
    Column('sourceaccountid', NUMBER(19, 0, False)),
    Column('destinationaccountid', NUMBER(19, 0, False)),
    Column('paymenttype', VARCHAR(20)),
    Column('amount', NUMBER(19, 4, True), nullable=False),
    Column('description', VARCHAR(120)),
    Column('sendsuccessnotification', VARCHAR(5)),
    Column('scheduledtransferid', NUMBER(19, 0, False)),
    Column('rundatetime', DateTime, nullable=False),
    Column('rundatetimeutc', DateTime, nullable=False),
    Column('completiondatetimeutc', DateTime),
    Column('succeeded', VARCHAR(5)),
    Column('operationsxml', Text),
    Column('submittedbyuserid', VARCHAR(32)),
    Column('contributionyear', VARCHAR(20)),
    schema='COCCDM'
)


t_xfr_transfer_achview = Table(
    'xfr_transfer_achview', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('type', VARCHAR(20)),
    Column('dataspace', VARCHAR(10)),
    Column('userid', VARCHAR(32)),
    Column('amount', NUMBER(19, 4, True), nullable=False),
    Column('rundatetime', DateTime, nullable=False),
    Column('rundatetimeutc', DateTime, nullable=False),
    Column('completiondatetimeutc', DateTime),
    Column('succeeded', VARCHAR(5)),
    Column('individualname', VARCHAR(22)),
    Column('achtransactiontype', VARCHAR(20)),
    Column('externalroutingnumber', VARCHAR(9)),
    Column('externalachaccountnumber', VARCHAR(24)),
    Column('externalachaccounttype', VARCHAR(20)),
    Column('internalachaccountnumber', VARCHAR(24)),
    Column('internalachaccounttype', VARCHAR(20)),
    Column('recurring', VARCHAR(5)),
    Column('achbatchid', NUMBER(19, 0, False)),
    Column('riskscore', NUMBER(10, 0, False), nullable=False),
    Column('creditcount', NUMBER(10, 0, False), nullable=False),
    Column('creditamount', NUMBER(19, 4, True), nullable=False),
    Column('debitcount', NUMBER(10, 0, False), nullable=False),
    Column('debitamount', NUMBER(19, 4, True), nullable=False),
    Column('institutionname', VARCHAR(36)),
    Column('routingnumber', VARCHAR(9)),
    Column('status', VARCHAR(9)),
    schema='COCCDM'
)


t_xfr_unlinkedaccount = Table(
    'xfr_unlinkedaccount', Base.metadata,
    Column('id', NUMBER(19, 0, False), nullable=False),
    Column('dataspace', VARCHAR(10)),
    Column('userid', VARCHAR(32)),
    Column('hostaccountid', VARCHAR(64)),
    Column('achaccountnumber', VARCHAR(24)),
    Column('achaccounttype', VARCHAR(20)),
    Column('regdlimited', VARCHAR(5)),
    Column('creationdatetimeutc', DateTime, nullable=False),
    Column('nickname', VARCHAR(120)),
    Column('deleted', VARCHAR(5)),
    Column('accountnumber', VARCHAR(40)),
    schema='COCCDM'
)
