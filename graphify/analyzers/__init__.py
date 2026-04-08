"""Graphify analyzers — language-specific code analysis plugins."""

from __future__ import annotations

from typing import TYPE_CHECKING

from graphify.core.schema import Language

if TYPE_CHECKING:
    from graphify.analyzers.base import BaseAnalyzer


def get_analyzer(language: Language) -> BaseAnalyzer | None:
    """Return the appropriate analyzer for a language, or None."""
    from graphify.analyzers.config_analyzer import ConfigAnalyzer  # pylint: disable=C0415
    from graphify.analyzers.doc_analyzer import DocAnalyzer  # pylint: disable=C0415
    from graphify.analyzers.generic_analyzer import GenericAnalyzer  # pylint: disable=C0415
    from graphify.analyzers.javascript_analyzer import JavaScriptAnalyzer  # pylint: disable=C0415
    from graphify.analyzers.python_analyzer import PythonAnalyzer  # pylint: disable=C0415

    _registry = {
        Language.PYTHON: PythonAnalyzer(),
        Language.JAVASCRIPT: JavaScriptAnalyzer(),
        Language.TYPESCRIPT: JavaScriptAnalyzer(),
        Language.YAML: ConfigAnalyzer(),
        Language.JSON: ConfigAnalyzer(),
        Language.TOML: ConfigAnalyzer(),
        Language.DOCKERFILE: ConfigAnalyzer(),
        Language.MARKDOWN: DocAnalyzer(),
        Language.HTML: GenericAnalyzer(),
        Language.CSS: GenericAnalyzer(),
        Language.SHELL: GenericAnalyzer(),
        Language.GO: GenericAnalyzer(),
        Language.RUST: GenericAnalyzer(),
        Language.JAVA: GenericAnalyzer(),
        Language.RUBY: GenericAnalyzer(),
        Language.CPP: GenericAnalyzer(),
        Language.C: GenericAnalyzer(),
        Language.CSHARP: GenericAnalyzer(),
        Language.SWIFT: GenericAnalyzer(),
        Language.KOTLIN: GenericAnalyzer(),
        Language.PHP: GenericAnalyzer(),
        Language.SQL: GenericAnalyzer(),
    }
    return _registry.get(language)
