# Planificacion de pruebas de la API de tareas

Esta tabla define los escenarios a cubrir antes de implementar los tests. Los casos asumen respuestas REST habituales en FastAPI; se deben ajustar si el contrato final de la API establece otros codigos o reglas.

| Endpoint | Tipo de caso | Escenario y datos | Resultado esperado |
|---|---|---|---|
| `GET /tasks` | Camino feliz | Hay varias tareas registradas. | `200 OK`; devuelve una lista con las tareas y sus campos esperados. |
| `GET /tasks` | Limite | No hay tareas registradas. | `200 OK`; devuelve una lista vacia (`[]`). |
| `GET /tasks` | Error | Ocurre un fallo inesperado al consultar el almacenamiento. | `500 Internal Server Error`; no expone detalles internos del fallo. |
| `POST /tasks` | Camino feliz | Se envia un cuerpo valido con los campos requeridos para crear una tarea. | `201 Created`; devuelve la tarea creada con su identificador y valores persistidos. |
| `POST /tasks` | Limite | Se envia el cuerpo valido mas pequeno permitido, usando valores por defecto o campos opcionales cuando corresponda. | `201 Created`; crea la tarea y aplica los valores por defecto definidos por el contrato. |
| `POST /tasks` | Error | Se envia un cuerpo invalido o falta un campo requerido. | `422 Unprocessable Entity`; informa del error de validacion y no crea una tarea. |
| `PATCH /tasks/{task_id}` | Camino feliz | Existe la tarea y se envia un cambio valido para uno o mas campos. | `200 OK`; devuelve la tarea actualizada y conserva sin cambios los campos omitidos. |
| `PATCH /tasks/{task_id}` | Limite | Existe la tarea y se envia un cuerpo vacio. | `200 OK`; la tarea se mantiene sin cambios. |
| `PATCH /tasks/{task_id}` | Error | El identificador no corresponde a una tarea existente. | `404 Not Found`; no modifica ninguna tarea. |
| `DELETE /tasks/{task_id}` | Camino feliz | Existe la tarea indicada. | `204 No Content`; elimina la tarea y no devuelve cuerpo. |
| `DELETE /tasks/{task_id}` | Limite | Se elimina la unica tarea existente. | `204 No Content`; la eliminacion termina correctamente y la lista queda vacia. |
| `DELETE /tasks/{task_id}` | Error | El identificador no corresponde a una tarea existente. | `404 Not Found`; no elimina ni altera otras tareas. |

## Supuestos por confirmar

- La creacion devuelve `201`, la consulta y actualizacion devuelven `200`, y la eliminacion devuelve `204`.
- FastAPI devuelve `422` ante errores de validacion del cuerpo.
- Una tarea inexistente produce `404` en `PATCH` y `DELETE`.
- Un cuerpo vacio en `PATCH` se acepta como una operacion sin cambios y devuelve `200`.
- Los campos requeridos, valores por defecto y restricciones dependen del esquema y del contrato que se definan para la API.