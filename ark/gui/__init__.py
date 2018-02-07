try:
    from PyQt4.QtWebKit import QWebPage
    QWK_AVAILABLE = True
except ImportError:
    QWK_AVAILABLE = False
from .action_settings_tool import ActionSettingsTool
from .base_map_widget import BaseMapWidget
from .data_dock import DataDock
if QWK_AVAILABLE:
    from .data_widget import DataWidget
from .digitising_widget import DigitisingWidget
from .feature_error_dialog import FeatureErrorDialog
from .feature_widget import FeatureWidget
from .figure_widget import FigureWidget
from .filter_clause_widget import FilterClauseWidget
from .filter_dock import FilterDock
from .filter_export_dialog import FilterExportDialog
from .filter_set_widget import FilterSetWidget
from .identify_item_action import IdentifyItemAction
from .layer_tree_menu import LayerTreeMenu
from .open_ark_action import OpenArkAction
from .plan_dock import PlanDock
from .plan_widget import PlanWidget
from .project_dialog import ProjectDialog
from .project_widget import ProjectWidget
from .schematic_widget import SchematicWidget
from .select_drawing_dialog import SelectDrawingDialog
from .select_item_dialog import SelectItemDialog
from .select_item_widget import SelectItemWidget
from .settings_dialog import SettingsDialog
from .settings_wizard import SettingsWizard
from .snapping_widget import SnappingWidget
from .source_widget import SourceWidget
from .trench_dock import TrenchDock
from .trench_widget import TrenchWidget
