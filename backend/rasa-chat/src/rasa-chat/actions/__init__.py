"""Inicialización del paquete de Actions.

Se eliminan las dependencias de Prometheus y se proveen métricas no-op
para mantener el código estable sin requerir la librería.
"""

class _NoopMetric:
    def labels(self, **_kwargs):
        return self

    def inc(self, *_args, **_kwargs):
        pass

    def observe(self, *_args, **_kwargs):
        pass

# Métricas no-op para que el resto del código pueda llamar labels/inc/observe
ACTION_INVOCATIONS = _NoopMetric()
ACTION_DURATION = _NoopMetric()