
- **app.py**

- **test_endpoints.py**
    - Function: `create_order`
  - Class: `DummyUpdatePaidUserDBRequest`
    - Function: `send_dummy_update_paid_user_db_request`
    - Function: `main`

### `database`

- **database\handle_orders_db_updates.py**
    - Function: `check_existing_order`
    - Function: `insert_new_order`

- **database\handle_user_db_updates.py**
    - Function: `delete_user_from_supabase`
    - Function: `add_user_to_supabase`

- **database\supabase_utils.py**
    - Function: `create_supabase_client`

### `models`

- **models\clerk_webhook_model.py**
  - Class: `LinkedTo`
  - Class: `Verification`
  - Class: `EmailVerification`
  - Class: `Email`
  - Class: `ExternalAccount`
  - Class: `BodyModel`
  - Class: `ClerkWebhookPayload`

- **models\orders_model.py**
  - Class: `Status`
  - Class: `PaymentPlatform`
  - Class: `Gender`
  - Class: `OrderData`
    - Function: `__post_init__`

- **models\user_model.py**
  - Class: `User`

- **models\webhook_model.py**
  - Class: `WebhookPayload`

- **models\__init__.py**

### `payments`

- **payments\lemon_squeezy_helpers.py**
    - Function: `get_product_id_from_pack_type_lmnsqzy`
    - Function: `generate_lemonsqueezy_payment_link`

- **payments\lemon_squeezy_webhook_handler.py**
    - Function: `verify_lemonsqueezy_signature`
    - Function: `process_lemon_squeezy_webhook`
    - Function: `validate_and_process_request_lemon_squeezy`

- **payments\process_payments_helper.py**
    - Function: `get_current_payment_mode_from_order_id`

- **payments\razory_pay_helpers.py**
    - Function: `get_razor_pay_prices_from_db`
    - Function: `get_razor_pay_pack_data`
    - Function: `create_razor_pay_order`

- **payments\razor_pay_webhook_handler.py**
    - Function: `validate_and_process_request_razorpay`

- **payments\__init__.py**

### `routes`

- **routes\basic_routes.py**
    - Endpoint: `basic_router.get`
      - Path: `/`
      - Function: `read_root`

- **routes\payments_routes.py**
    - Endpoint: `payments_router.post`
      - Path: `/payments/generate_payment_link`
      - Function: `process_payments`
    - Endpoint: `payments_router.get`
      - Path: `/payments/razorpay/get_razorpay_key`
      - Function: `get_razorpay_key`
  - Class: `RazorPayValidationRequest`
    - Endpoint: `payments_router.post`
      - Path: `/payments/razorpay/validate`
      - Function: `validate_razorpay_payment`

- **routes\webhook_routes.py**
    - Endpoint: `webhook_router.post`
      - Path: `/webhook/razorpay`
      - Function: `razorpay_webhook`
    - Endpoint: `webhook_router.post`
      - Path: `/webhook/lemonsqueezy`
      - Function: `lemonsqueezy_webhook`
    - Endpoint: `webhook_router.post`
      - Path: `/webhook/clerk`
      - Function: `clerk_webhook`
    - Endpoint: `webhook_router.post`
      - Path: `/webhook/clerk/prod`
      - Function: `clerk_webhook_prod`

- **routes\__init__.py**

### `slack_bot`

- **slack_bot\slackbot.py**
  - Class: `SlackBot`
    - Function: `__init__`
    - Function: `send_message`

- **slack_bot\__init__.py**

### `utils`

- **utils\config.py**
  - Class: `Settings`
    - Function: `__new__`

- **utils\give_structure.py**
    - Function: `read_gitignore_specs`
    - Function: `analyze_python_files`
    - Function: `analyze_and_write_file_structure`

- **utils\logger.py**
    - Function: `get_logger`

- **utils\utils.py**
    - Function: `convert_unix_to_datetime`

- **utils\__init__.py**
