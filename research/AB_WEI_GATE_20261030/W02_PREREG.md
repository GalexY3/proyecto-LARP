# W02 — Pre-registro AB-R: puerta CMake legada en entorno Linux actual (sin Wei)
Fecha 2026-10-30. Autorización actual: 10 AB-R, W01 auditoría inválida; no contar ciclos previstos. W02 es una prueba técnica controlada nueva, no una evaluación MHU.
A. Estimando: éxito binario de configure/build/run de un proyecto C++ mínimo, por tres contratos de versión CMake; población: este entorno Linux/CMake concreto, no Windows ni repositorio Wei completo.
B. H0: 2.6 sin override compila; H1: legacy falla y override min 3.5 lo corrige; H2: falla por motivos ajenos a políticas. Control competente: CMake 3.5 mínimo sobre mismo C++/toolchain.
C. 3 brazos fijados antes de resultados: legacy_2_6_no_flag, legacy_2_6_policy_min_3_5, modern_3_5_no_flag. Outcome primario configure returncode; secundarios build returncode, binario returncode y warnings. No repetir ni ajustar configuración después de outcome.
D. Código congelado en w02_cmake_probe.py (SHA de commit de GitHub precede a ejecución), test temporal aislado sin acceso a LARP. Captura cmake --version, g++ --version, platform, SHA256 del script y contenido generado.
E. Ejecutar una sola vez cada condición y archivar salida JSON sin recortes engañosos.
F. Control adversarial: un toy project que compila NO implica compilación de Wei, ni de sus dependencias, ni compatibilidad Windows; cualquier advertencia separada de fallo. No hay modelo neuronal.
G. Replicación: no realizada externamente; un equipo Windows y el log original siguen necesarios.
H. Prior: si legacy no falla aquí, no atribuir el fallo Windows automáticamente a mínimo 2.6; si sí falla, demostrarlo únicamente en este Linux/CMake.
I. CT2 matemática 24/100 y funcional 18/100 sin cambios; resultado técnico 0/3 en descubrimiento científico, independiente de su utilidad de diagnóstico.
J. AB-DECIDE: STOP_WEI_BUILD hasta logs originales/compilación de fuente exacta; nueve autorizaciones restantes tras W02 si es válida.
R1–R5; O1–O7, no CI, main intacto, presupuesto de duración por subprocess 15 segundos, sin red.
