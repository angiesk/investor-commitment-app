from enum import Enum


# Define UserType Enum
class UserType(Enum):
    INVESTOR = "investor"
    PREQUIN = "prequin"


class InvestorType(str, Enum):
    FUND_MANAGER = "fund_manager"
    ASSET_MANAGER = "asset_manager"
    WEALTH_MANAGER = "wealth_manager"
    BANK = "bank"


class AssetClass(str, Enum):
    Infrastructure = "Infrastructure"
    HedgeFunds = "Hedge Funds"
    PrivateEquity = "Private Equity"
    RealEstate = "Real Estate"
    Other = "Other"
