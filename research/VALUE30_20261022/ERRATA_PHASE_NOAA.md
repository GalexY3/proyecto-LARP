# ERRATA — Corrección de la interpretación del pivot NOAA / Niño 1+2

Fecha: 22-10-2026. Documento afectado: `DICTAMEN_AB30_VALUE.md` y prior `VAL30-R05`, primer commit del bloque VALUE30 `fbe8995ae4d51c8ef29e7fd4073b6797b85ed38b`.

**Afirmación previa incorrectamente generalizada:** "la regularidad temporal es perjudicial" / "refuta la universalidad de la regularidad".

**Corrección:** los calendarios [enero, abril, julio, octubre] y [febrero, mayo, agosto, noviembre] están ambos separados por tres meses. Por tanto el contraste RMSE test 0.242 °C vs 0.085 °C **NO aísla regularidad frente a irregularidad**, sino **la fase** de un muestreo regular ante un proceso estacional no invariante a traslación de calendario. El selector circulante puede ser indiferente a la fase; el selector que estima covarianza empírica aprende una fase más adecuada a este caso.

**Consecuencia epistemológica:** conservar el resultado cuantitativo, reemplazar la conclusión causal sobre regularidad por una conclusión condicional sobre fase. No usar estos datos para sostener que regularidad espacial/temporal es perjudicial, que MHU falla, ni que COSI multiclase ha sido verificado en un dato NOAA de una sola serie.

**Estado AB:** reparación explicativa POST_HOC, no nuevo ciclo ni confirmación; conservar historial y actualizar priors sin borrar la errata.
