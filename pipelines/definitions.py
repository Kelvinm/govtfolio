from dagster import Definitions, load_assets_from_modules
import logging
from . import assets

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Loading assets...")
all_assets = load_assets_from_modules([assets])
logger.info(f"Loaded {len(all_assets)} assets")

defs = Definitions(
    assets=all_assets
)
