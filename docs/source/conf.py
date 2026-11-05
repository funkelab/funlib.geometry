project = "funlib.geometry"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "myst_parser",
]
# Styled after the e11lib.ml docs: pydata theme, no sidebars, full width, and
# the system's light or dark mode.
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "show_nav_level": 3,
    "navigation_depth": 3,
    "collapse_navigation": True,
}
html_sidebars = {"**": []}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
autodoc_member_order = "bysource"
myst_heading_anchors = 3
