from dotenv import load_dotenv
import os

load_dotenv()
class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.LEMONSQUEEZY_WEBHOOK_SECRET = os.getenv('LEMONSQUEEZY_WEBHOOK_SECRET')
            cls._instance.SUPABASE_URL = os.getenv('SUPABASE_URL')
            cls._instance.SUPABASE_KEY = os.getenv('SUPABASE_KEY')
            cls._instance.SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
            cls._instance.RAZOR_PAY_ID = os.getenv('RAZOR_PAY_ID')
            cls._instance.IS_TEST_MODE = os.getenv('IS_TEST_MODE', 'False').lower() in ('true', '1', 't')
            cls._instance.LEMONSQUEEZY_BASIC_TEST_PRODUCT_ID = os.getenv('LEMONSQUEEZY_BASIC_TEST_PRODUCT_ID')
            cls._instance.LEMONSQUEEZY_STANDARD_TEST_PRODUCT_ID = os.getenv('LEMONSQUEEZY_STANDARD_TEST_PRODUCT_ID')
            cls._instance.LEMONSQUEEZY_PRO_TEST_PRODUCT_ID = os.getenv('LEMONSQUEEZY_PRO_TEST_PRODUCT_ID')
            cls._instance.LEMONSQUEEZY_BASIC_PRODUCT_ID = os.getenv('LEMONSQUEEZY_BASIC_PRODUCT_ID')
            cls._instance.LEMONSQUEEZY_STANDARD_PRODUCT_ID = os.getenv('LEMONSQUEEZY_STANDARD_PRODUCT_ID')
            cls._instance.LEMONSQUEEZY_PRO_PRODUCT_ID = os.getenv('LEMONSQUEEZY_PRO_PRODUCT_ID')
            cls._instance.is_razor_pay_test_mode = True if cls._instance.RAZOR_PAY_ID.startswith('rzp_test') else False
            cls._instance.is_clerk_test_mode:bool
        return cls._instance

    
settings = Settings()
print(settings.LEMONSQUEEZY_BASIC_PRODUCT_ID)
# settings.is_razor_pay_test_mode = True if settings.RAZOR_PAY_ID.startswith('rzp_test') else False

# print("RUNNNNNNNNNNONG")
# if settings.IS_TEST_MODE == "True":
#     settings.IS_TEST_MODE = True
# elif settings.IS_TEST_MODE == "False":
#     settings.IS_TEST_MODE = False

