# AB20 QuixBugs — reporte de cierre

**20 ciclos A–J ejecutados**, 20 algoritmos defectuosos escritos por terceros como retos Quixey Challenge, no errores de producción. Código upstream fijado a commit `4257f44b0ff1181dedaedee6a447e133219fcebf`, source local del motor R1 SHA256 `db5dc62aa1c5fe2f08b3ac233582493808d75c95793ed87f6fdcbb05a70f8a57`; pruebas y snippets están en ZIP de conversación, pendiente de subida remota íntegra.

**E (3 permutaciones de un pool manual de 12 casos/algoritmo):** chequeos superficiales 8/20; metamórficos 13/20; comparación con programa corregido 20/20. Ensayos programa-semilla: 22/60, 36/60, 56/60. 
**G (5 permutaciones nuevas del MISMO pool):** 8/20; 13/20; 20/20. Ensayos programa-semilla: 37/100, 54/100, 94/100. 
**Reparación R1:** E v1 se invalidó porque el test superficial exigía el tipo de resultado equivocado en gcd y get_factors (6 falsas alarmas programa-semilla), y una propiedad falsa para lcs_length generó una alarma adicional. Fuente v1 SHA256 `7999be6213a8223ecd904ee39cee5816a215589275ca735a6c3b4f91cc3a608a`. Antes de repetir E y abrir G, el parche exacto y hash R1 se congelaron en [prereg/REPAIR_R1_NEGATIVE_CONTROLS.md](../prereg/REPAIR_R1_NEGATIVE_CONTROLS.md). Tras reparación, **0 falsas alarmas sobre versiones reparadas en 480 combinaciones programa/semilla/estrategia**.

**Observación:** M detecta cinco programas más que S, diferencia emparejada +25 pp en estos veinte problemas no aleatorios. Intervalo bootstrap descriptivo por programa +5 a +45 pp; contraste exacto bilateral por cinco pares discordantes p=0,0625 sin corrección, no inferencia poblacional. M omite siete defectos que O detecta. **O posee el programa corregido**, por lo que no tiene paridad de información ni de coste total con S/M pese a igualar seis ejecuciones de la versión defectuosa. Se usaron casos preparados con conocimiento de los contratos: no se trató de un benchmark ciego.

**Prior art:** QuixBugs (Lin et al. 2017); MR-Scout (ACM TOSEM 2024); SFIDMT-ART (IST 2024), además de décadas de testing metamórfico. La metodología no es novedosa. Tampoco hay incidencias reales de producción ni reproducciones con herramientas profesionales como Hypothesis a igual coste.

**Balance:** CT2 de esta línea 13→11/100, ordinal, no probabilidad. Un único hallazgo local técnico 1/3 `QB-MR-06` conservado en registro acumulativo de LARP con todos los falsadores; 2/3=0; 3/3=0. La campaña R1 es exploratoria tras exposición previa E; G usa el mismo conjunto de casos, no aporta independencia externa.

**Próxima puerta:** defectos reales de proyectos científicos externos, diseño ciego de relaciones antes de consultar el arreglo, y controles profesionales de igual presupuesto de tiempo e información. **AB-DECIDE: CLOSE20, SOLICITO BRANCHING 20 CICLOS.**
