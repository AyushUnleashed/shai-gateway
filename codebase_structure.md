
- **app.py**

- **test_endpoints.py**
    - Function: `create_order`
  - Class: `DummyUpdatePaidUserDBRequest`
    - Function: `send_dummy_update_paid_user_db_request`
    - Function: `main`

### `image_generator`

- **image_generator\replicate_face_swap_api_call.py**
    - Function: `perform_face_swap_and_save_simple`
    - Function: `main`

- **image_generator\sd_image_gen.py**
    - Function: `get_prompt`
    - Function: `handle_sd_image_generation`
    - Function: `call_sd_api_replicate`

- **image_generator\__init__.py**

### `image_generator\utils`

- **image_generator\utils\constants.py**
    - Function: `set_user_image_path`

- **image_generator\utils\image_gen_utils.py**
    - Function: `get_all_pose_names`

- **image_generator\utils\prompts.py**

- **image_generator\utils\text_box.py**
    - Function: `add_text_box`
    - Function: `main`

- **image_generator\utils\__init__.py**

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

### `notification`

- **notification\gmail_service.py**
    - Function: `send_email`
    - Function: `send_image_via_gmail`

- **notification\slackbot.py**
  - Class: `SlackBot`
    - Function: `__init__`
    - Function: `send_message`

- **notification\__init__.py**

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
    - Endpoint: `basic_router.post`
      - Path: `/update_paid_user_db`
      - Function: `update_paid_user_order_with_details`
    - Endpoint: `basic_router.post`
      - Path: `/generate_free_image`
      - Function: `generate_free_image`
    - Endpoint: `basic_router.post`
      - Path: `/get_user_credits`
      - Function: `get_user_credits`

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
    - Endpoint: `webhook_router.post`
      - Path: `/webhook/replicate`
      - Function: `replicate_webhook`
    - Function: `process_replicate_webhook`

- **routes\__init__.py**

### `supabase_tools`

- **supabase_tools\handle_image_bucket_updates.py**
    - Function: `handle_supabase_upload`
    - Function: `get_bucket_image_url`

- **supabase_tools\handle_image_tb_updates.py**
    - Function: `make_image_db_entry`
    - Function: `get_image_id_user_id_from_prediction_id`
    - Function: `update_db_with_final_image_link`

- **supabase_tools\handle_orders_db_updates.py**
    - Function: `check_existing_order`
    - Function: `insert_new_order`

- **supabase_tools\handle_user_db_updates.py**
    - Function: `delete_user_from_supabase`
    - Function: `add_user_to_supabase`
    - Function: `get_user_current_credits`
    - Function: `reduce_user_credits`
    - Function: `get_user_email_from_user_id`

- **supabase_tools\supabase_utils.py**
    - Function: `create_supabase_client`

- **supabase_tools\__init__.py**

### `utils`

- **utils\config.py**
  - Class: `Settings`
    - Function: `__new__`

- **utils\constants.py**

- **utils\give_structure.py**
    - Function: `read_gitignore_specs`
    - Function: `analyze_python_files`
    - Function: `analyze_and_write_file_structure`

- **utils\logger.py**
    - Function: `get_logger`

- **utils\utils.py**
    - Function: `convert_unix_to_datetime`

- **utils\__init__.py**
