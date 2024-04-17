from pydantic import FilePath, DirectoryPath
from image_generator.utils.image_gen_utils import get_all_pose_names

DEFAULT_CONTROL_TYPE: str = "pose"
DEFAULT_BASE_MODEL: str = "digiplay/Juggernaut_final"


DEFAULT_NEGATIVE_PROMPT: str = ''' (close up) ((mask)) ((helmet)), signature, watermark, disfigured, kitsch, ugly, oversaturated, grain, low-res, Deformed, blurry, 
bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, ugly, poorly drawn 
hands, missing limb, blurry, floating limbs, disconnected limbs, malformed hands, blur, 
out of focus, long neck, long body, ugly, disgusting, poorly drawn, childish, mutilated, mangled, 
old, surreal, long face, full body, out of frame'''


PROMPT_SUFFIX = "sharp details, realistic textures, cinematic quality, realism and depth,in action-packed poses, emotion and intensity, photorealistic, ultra hd, 8k"

USER_IMAGE_PATH: FilePath | None = None

def set_user_image_path(image_path: FilePath):
    global USER_IMAGE_PATH
    USER_IMAGE_PATH = image_path

POSE_DIRECTORY_PATH: DirectoryPath = "image_generator/assets/poses"
USER_CONTENT_DIRECTORY_PATH: DirectoryPath = "image_generator/user_content"
POSE_SET=get_all_pose_names('image_generator/assets/poses')

S3_REMOTE_DIRECTORY_PATH: str = "https://superhero-ai-bucket.s3.ap-south-1.amazonaws.com/"