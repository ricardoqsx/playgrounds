# AGENTS.md - Guia operativa para agentes de desarrollo

Este documento define como debe trabajar un agente dentro de este repositorio para mantener foco, consistencia tecnica, entregas verificables y bajo desperdicio de tokens. Las reglas son genericas y deben adaptarse al stack, arquitectura y objetivos reales del proyecto activo.

## 1) Principios generales

- Entender primero el objetivo del usuario, el modulo afectado, la entrada de datos, la salida esperada y los criterios de aceptacion.
- Inspeccionar el codigo existente antes de asumir arquitectura, nombres, dependencias o convenciones.
- Preferir el cambio minimo correcto sobre reingenieria amplia.
- Mantener separacion clara entre acceso a datos, reglas de negocio, presentacion, estilos y comportamiento de interfaz.
- No asumir datos perfectos: manejar nulos, entradas invalidas, fechas mal formadas, respuestas vacias y registros incompletos.
- Respetar el stack existente. No introducir frameworks, servicios, dependencias o patrones nuevos sin necesidad concreta.
- Toda decision tecnica debe poder justificarse por mantenibilidad, seguridad, operacion, claridad o tiempo de respuesta.

## 2) Comunicacion y uso de tokens

- Comunicar de forma compacta, directa y util.
- Evitar imprimir contenido innecesario en pantalla.
- No pegar archivos completos, diffs largos, logs extensos ni salidas completas de comandos si no aportan a la decision.
- Resumir hallazgos y mostrar solo rutas, errores, comandos ejecutados y resultados relevantes.
- Usar busquedas, lecturas por rango y filtros especificos para evitar ruido.
- No narrar pasos obvios ni repetir contexto ya establecido.
- No exponer razonamiento completo, cadenas de pensamiento ni analisis paso a paso salvo solicitud explicita de explicacion tecnica detallada.
- Si existen varias alternativas validas, recomendar una principal y explicar brevemente por que.
- Ampliar detalles solo cuando sean necesarios para justificar una decision importante, documentar un riesgo o responder una pregunta directa.

## 3) Flujo de trabajo

Antes de iniciar:
- Confirmar que la tarea corresponde al alcance solicitado.
- Identificar archivos, capas y contratos afectados.
- Revisar convenciones existentes, documentacion local y pruebas disponibles.
- Si existe `PLAN.md` o carpeta `plan/`, revisarlos para tareas relevantes. Si no existen, no crearlos ni asumir roadmap salvo instruccion del usuario.

Durante la implementacion:
- Trabajar cada caracteristica como una unidad revisable.
- Evitar mezclar cambios no relacionados en el mismo bloque de trabajo.
- Mantener nombres explicativos y consistentes con el dominio del proyecto.
- Comentar el codigo solo cuando una regla, decision o bloque no sea evidente.
- No duplicar logica existente; reutilizar funciones, servicios o componentes ya presentes.
- Si aparecen cambios ajenos en el worktree, no revertirlos ni modificarlos salvo instruccion explicita.

Antes de cerrar:
- Ejecutar validaciones razonables segun el proyecto: pruebas, linters, type checks, comandos de build o consultas manuales.
- Si existe `PLAN.md` o `plan/`, marcar checkboxes solo cuando el cambio realmente complete el hito con implementacion y validacion suficiente.
- Revisar si hay documentacion interna que deba actualizarse.
- Reportar objetivo, archivos tocados, cambios clave, validacion y riesgos solo con el detalle necesario.

## 4) Git y trabajo colaborativo

- El usuario gestiona ramas, commits, merges, rebases, tags y pushes.
- No ejecutar commits, amend, merges, rebases, tags ni pushes salvo instruccion explicita.
- Trabajar sobre la rama activa.
- No usar comandos destructivos como `git reset --hard` o restauraciones masivas salvo aprobacion explicita.
- Si una tarea puede requerir una rama especifica o afectar trabajo paralelo, confirmar alcance antes de editar.
- Nunca revertir cambios que no fueron hechos por el agente salvo que el usuario lo pida directamente.

## 5) Seguridad aplicativa

- No registrar contrasenas, hashes, tokens, cookies, secretos ni payloads sensibles completos.
- Validar autorizacion en backend para rutas, endpoints y acciones sensibles; el frontend solo mejora la experiencia de usuario.
- Cuando existan sesiones/cookies, formularios `POST` o endpoints `POST`/`PUT`/`PATCH`/`DELETE` que modifiquen datos, implementar proteccion CSRF antes de cerrar la funcionalidad.
- Para APIs JSON con cookies de sesion, usar un token CSRF enviado por header estable cuando aplique.
- Definir permisos por rol/perfil/capacidad antes de exponer administracion, exportaciones, datos sensibles o acciones destructivas.
- Auditar acciones sensibles cuando el proyecto tenga auditoria o el alcance lo requiera.
- Sanitizar parametros antes de registrarlos en logs o auditoria.
- No agregar mecanismos de seguridad por inercia si todavia no aplican, pero no cerrar acciones autenticadas o mutaciones sin las protecciones necesarias.

## 6) Backend

Aplicar estas reglas cuando el proyecto tenga backend, APIs o servicios HTTP:

- `routes/`, `controllers/` o capa HTTP:
  - Leer y validar parametros basicos de request.
  - Llamar funciones de servicios, casos de uso o modelos segun la arquitectura existente.
  - Devolver respuestas HTTP/JSON.
  - No escribir SQL ni reglas de negocio complejas en esta capa.

- `services/`, `use_cases/` o capa de aplicacion:
  - Orquestar reglas de negocio y validaciones de dominio.
  - Transformar y normalizar payloads.
  - Coordinar llamadas a modelos, repositorios o clientes externos.
  - No depender de objetos HTTP cuando pueda evitarse.

- `models/`, `repositories/` o capa de datos:
  - Encapsular consultas, persistencia y acceso a fuentes de datos.
  - Usar consultas parametrizadas o APIs seguras del ORM/query builder.
  - Evitar dependencias de request/response.

- `utils/`, `lib/` o helpers compartidos:
  - Mantener funciones transversales pequenas y reutilizables.
  - Evitar convertir utilidades en una capa de negocio oculta.

- Criterio pragmatico:
  - Si una ruta es simple y la arquitectura lo permite, se acepta `HTTP -> datos` con validacion minima.
  - Si hay reglas de negocio, multiples consultas, transformaciones o normalizacion, usar una capa intermedia.
  - Elegir la ruta mas simple que conserve claridad y mantenibilidad.

- Calidad por endpoint:
  - Definir contrato de entrada/salida.
  - Mantener JSON estable en claves y tipos, sin depender del orden de campos.
  - Cubrir casos minimos: valido, sin datos, invalido y error controlado.

## 7) Datos, rendimiento y observabilidad

- Antes de optimizar rendimiento, medir con evidencia: latencia, consultas dominantes, volumen de datos, cache hit/miss o escenarios reales.
- Priorizar soluciones simples: consultas indexables, indices adecuados, paginacion, agregados locales o cache de servicio cuando haya evidencia.
- No introducir caches externos, colas, replicas, workers o infraestructura distribuida sin necesidad concreta o hito planificado.
- Las tablas derivadas, caches o agregados deben poder reconstruirse desde una fuente de verdad clara.
- Los procesos de reconstruccion o mantenimiento deben ser idempotentes y trazables.
- Los logs deben ser utiles, estables y no filtrar secretos.
- Evitar requests pesados por defecto; pedir solo los datos necesarios para la vista o accion activa.

## 8) Frontend

Aplicar estas reglas cuando el proyecto tenga frontend, plantillas o interfaz web:

- Estructura:
  - Separar estructura HTML/templates, estilos y comportamiento JavaScript/TypeScript.
  - No duplicar reglas de negocio que pertenecen al backend.
  - Mantener componentes o modulos pequenos por responsabilidad.

- Estilos:
  - Respetar el sistema visual existente.
  - No introducir frameworks CSS, librerias UI o assets externos sin necesidad clara.
  - No depender de CDN para recursos base salvo decision explicita del proyecto.
  - Si se adapta una plantilla externa, extraer solo lo necesario y evitar copiar reglas globales que puedan romper la interfaz existente.

- Comportamiento:
  - Separar comportamiento global de shell/layout del comportamiento propio de cada vista.
  - Manejar estados de carga, vacio, error HTTP y respuesta sin datos.
  - No ocultar errores de contrato con fallbacks silenciosos que dificulten depuracion.

- Contrato con backend:
  - Consumir endpoints documentados o inferidos del codigo existente.
  - No depender del orden de campos en JSON.
  - Mantener compatibilidad solo cuando exista necesidad real: datos persistidos, usuarios externos o requerimiento explicito.

- Responsive y accesibilidad:
  - Verificar que la vista sea usable en desktop y mobile cuando aplique.
  - Mantener controles claros, labels utiles, estados visibles y navegacion consistente.

## 9) Documentacion

- Cada carpeta funcional deberia tener un `README.md` interno cuando el proyecto lo use o cuando la complejidad lo justifique.
- Al modificar funciones, endpoints, servicios, modelos, componentes, plantillas o archivos frontend relevantes, revisar si la documentacion de la carpeta tambien debe actualizarse.
- La documentacion debe explicar proposito, responsabilidades, contratos principales, relacion con otras capas y reglas de mantenimiento.
- La documentacion no reemplaza nombres claros, pruebas ni docstrings utiles.
- No crear documentacion extensa por inercia; documentar lo necesario para mantener el proyecto operable.

## 10) Validacion

- Elegir validaciones proporcionales al cambio.
- Preferir pruebas automatizadas existentes antes de crear flujos manuales largos.
- Si no hay pruebas, ejecutar comandos disponibles o validar manualmente el camino afectado.
- Registrar evidencia breve: comando ejecutado, resultado y cualquier limitacion.
- No declarar una tarea lista si no se pudo validar lo esencial; explicar el bloqueo o riesgo.

## 11) Formato de entrega

Para cambios relevantes o no triviales, reportar de forma breve:

1. Objetivo: que se implemento o corrigio.
2. Archivos tocados: rutas modificadas.
3. Cambios clave: decisiones y logica aplicada.
4. Validacion: pruebas o comandos ejecutados y resultado.
5. Riesgos o pendientes: limites conocidos y siguiente paso recomendado.

Para cambios simples, usar una version resumida con resultado y validacion.

---

Si hay conflicto entre este archivo y una instruccion explicita mas reciente del usuario, prevalece la instruccion del usuario dentro del alcance solicitado.
