class BaseRole(object):
    pass


class UndefinedRole(object):
    def __init__(self):
        super(UndefinedRole, self).__init__()


class LandlordRole(BaseRole):
    def __init__(self):
        super(LandlordRole, self).__init__()


class FarmerRole(BaseRole):
    def __init__(self):
        super(FarmerRole, self).__init__()
