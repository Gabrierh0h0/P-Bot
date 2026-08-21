  
**MAKERS AI PRODUCT**

**Sesión 5 — Problem thesis \+ AI flow v0**  
**Instrucciones**

Hagan una copia de este documento.

Renombren el archivo: Equipo X \- Makers AI Product.  
Completen todas las secciones.  
Sean concretos.  
No escriban “la IA analiza” o “devuelve una respuesta” sin explicar qué significa.  
Al final preparen un pitch de 2 minutos.

1\. Equipo  
Nombre del equipo: Popxye’s  
Integrantes: Gabriel Alejandro Giraldo Ayerbe y Luis Miguel Brito Rincon  
Nombre provisional del proyecto: PeterBot

2\. Problem thesis

Creemos que los dueños/encargados de restaurantes pequeños y medianos tienen dificultades para procesar pedidos que llegan por WhatsApp, porque el proceso es manual (leer el chat, anotar el pedido, calcular el total, confirmar dirección y forma de pago uno por uno), lo que genera errores en los pedidos, demoras en horas pico, pedidos incompletos y pérdida de ventas.  
Usuario: Encargado(a) de pedidos o dueño de un restaurante pequeño/mediano que recibe pedidos por WhatsApp  
Problema o dolor: Pierde tiempo y comete errores gestionando pedidos manualmente por chat: direcciones incompletas, falta el medio de pago, el total se calcula mal, o el pedido queda ambiguo ("la de siempre", "sin cebolla porfa")  
Cómo lo resuelve actualmente: Una persona lee cada mensaje de WhatsApp, transcribe el pedido a mano en una libreta o en una hoja de Excel, calcula el total manualmente y responde uno por uno para confirmar  
Por qué la solución actual no es suficiente: Es lento, depende de que siempre haya alguien disponible respondiendo, no escala en horas pico y los errores humanos generan pedidos mal preparados, reclamos y pérdida de confianza del cliente

3\. ¿Por qué usar IA?  
**Capacidades necesarias:**

☑ Extraer información

☑ Clasificar

☑ Comparar

☐ Resumir

☑ Generar

☐ Recomendar

☑ Evaluar

☐ Planear

☑ Trabajar con texto, imagen, audio o documentos (texto y notas de voz)

**La ventaja específica de usar IA sería:** Entender lenguaje natural no estructurado, tal como la gente realmente escribe en WhatsApp (con errores de digitación, abreviaturas, notas de voz, mensajes en varias partes), y convertirlo automáticamente en un pedido estructurado, validado contra el menú real y disponible las 24 horas, sin depender de una persona conectada todo el tiempo

4\. Input  
**¿Qué recibe el sistema?:** Un mensaje de WhatsApp del cliente con su pedido en lenguaje natural (texto libre, y opcionalmente una nota de voz transcrita)

**Quién entrega el input:** El cliente final, directamente por WhatsApp

**Formato:** Texto libre (chat de WhatsApp); opcionalmente audio transcrito a texto

**Información obligatoria:** Producto(s) deseados, cantidad, dirección de entrega, nombre del cliente y medio de pago

**Contexto adicional necesario:** Menú vigente del restaurante con precios y disponibilidad, zonas de cobertura de domicilio, horario de atención y promociones activas

**Ejemplo real de input:** "Hola buenas\! Quiero 2 hamburguesas sencillas sin cebolla y una limonada grande, para la Cra 45 \#12-30, pago con Nequi 

5\. AI flow v0  
**El usuario entrega:** El pedido en texto libre por WhatsApp (y datos de contacto asociados al número)

**El sistema valida:** Que el mensaje contenga los datos mínimos (producto, dirección, medio de pago); si falta algo, el bot responde pidiendo puntualmente el dato faltante

**El sistema agrega contexto:** Menú actualizado con precios y disponibilidad, zona de cobertura de domicilios, horario de atención y promociones vigentes

**La IA extrae o identifica:** Productos solicitados, cantidades, modificaciones/exclusiones (ej. "sin cebolla"), dirección, nombre del cliente y medio de pago

**La IA analiza, compara o genera:** Compara cada producto mencionado contra el menú real (nombre, disponibilidad, precio), calcula subtotal, costo de domicilio y total, y genera un resumen estructurado del pedido; si un producto no existe o no está disponible, sugiere alternativas del menú

**El sistema verifica:** Que el total sume correctamente, que la dirección esté dentro de la zona de cobertura y que el medio de pago sea uno de los aceptados por el restaurante

**El usuario recibe:** Un resumen de confirmación del pedido con el detalle de productos, el total a pagar, el tiempo estimado de entrega y los medios de pago disponibles

**Después del resultado ocurre:** El pedido confirmado se envía automáticamente al sistema de cocina/POS del restaurante para su preparación, y se genera un registro para la persona encargada del domicilio

6\. Output esperado  
El sistema debe devolver:  
Devuelve únicamente JSON válido con lo que se encuentra en los campos

| Campo o sección                   	 | Contenido |
| :---- | :---- |
| Cliente | Nombre y teléfono de contacto |
| Productos | Lista de productos, cantidad y modificaciones/exclusiones por producto |
| Subtotal | Suma del valor de los productos |
| Costo de domicilio | Valor del envío según la zona |
| Total | Subtotal \+ domicilio |
| Dirección de entrega | Dirección validada dentro de la zona de cobertura |
| Medio de pago | Uno de los medios aceptados por el restaurante |
| Tiempo estimado de entrega | Minutos estimados según carga actual de cocina |
| Requiere revisión humana | Sí/No, según si hubo ambigüedad o datos faltantes |

**Ejemplo ideal del output:** "Tu pedido: 2 Hamburguesas sencillas (sin cebolla) $36.000 \+ 1 Limonada grande $8.000. Subtotal: $44.000. Domicilio: $5.000. Total: $49.000. Entrega en Cra 45 \#12-30. Pago: Nequi. Tiempo estimado: 35 min. ¿Confirmas tu pedido?"

7\. Riesgo principal  
**Qué podría salir mal:** La IA interpreta mal un producto ambiguo, inventa un producto o precio que no existe en el menú, o confunde/asume mal una dirección incompleta

**Consecuencia:** El cliente recibe un pedido incorrecto o mal cobrado, la entrega falla por dirección errónea, y el restaurante pierde tiempo y confianza del cliente

**Cómo lo controlaremos:** El menú oficial (con precios) es siempre la fuente de verdad, nunca un dato que la IA pueda inventar; cualquier producto que no coincida exactamente con el menú o cualquier dirección incompleta marca el pedido como "requiere\_revision" y lo envía a un humano antes de pasar a cocina; además, el bot siempre muestra el resumen del pedido al cliente para que lo confirme antes de procesarlo

8\. Criterio de éxito  
Sabremos que funciona si logra confirmar pedidos completos y correctos, sin intervención humana, para el cliente que escribe por WhatsApp.

**Métrica principal:** Porcentaje de pedidos procesados automáticamente sin error ni corrección humana

**Resultado mínimo aceptable:** 80% de los pedidos quedan correctamente estructurados en el primer intento

**Señal de valor para el usuario:** Se reduce notoriamente el tiempo entre que el cliente escribe el pedido y que este queda confirmado en cocina, y el restaurante deja de perder ventas por errores o demoras en la atención por chat

9\. Pitch de 2 minutos  
PeterBot es un agente de WhatsApp para restaurantes que recibe pedidos escritos en lenguaje natural por los clientes, los interpreta contra el menú real del restaurante, valida dirección y medio de pago, calcula el total automáticamente y confirma el pedido con el cliente antes de enviarlo a cocina. La IA aporta valor porque entiende el lenguaje informal y desordenado con el que la gente realmente pide comida por chat, y lo convierte en un pedido estructurado sin necesidad de que un humano esté siempre disponible. El input es el mensaje de WhatsApp del cliente; el flujo valida, extrae, compara contra el menú, calcula el total y verifica cobertura y forma de pago; el output es la confirmación del pedido con todos los datos necesarios para prepararlo y entregarlo. El riesgo principal es que la IA invente un producto o precio inexistente, por lo que el menú siempre es la fuente de verdad y cualquier ambigüedad se marca para revisión humana. Sabremos que funciona si al menos el 80% de los pedidos se procesan correctamente sin intervención humana.

Checklist final  
☑ El usuario es específico.

☑ El problema es claro.

☑ Hay un ejemplo real de input.

☑ El flujo tiene pasos concretos.

☑ Está claro qué hace la IA.

☑ El output tiene campos definidos.

☑ Hay un riesgo relevante.

☑ El éxito puede medirse.

☑ El output puede convertirse después en JSON.

# Sesión 6 — JSON & Structured Outputs

**Instrucciones**

1. Abran el documento de la sesión anterior.  
2. Revisen su **AI flow v0**.  
3. Revisen su **output esperado**.  
4. Definan quién consume ese output.  
5. Diseñen primero los campos.  
6. Después creen su JSON.  
7. Prueben el resultado con un input real.  
8. Prueben también un caso ambiguo o incompleto.  
9. Corrijan al menos un error encontrado.  
10. Al final preparen un pitch de 2 minutos.

1\. Identificación

**Equipo:**

Equipo: Popxye’s

Nombre del proyecto: PeterBot

Nombre del output: pedido\_whatsapp

Ejemplo: pedido\_whatsapp\_20260730\_001

2\. Output anterior

Copien el output esperado que definieron en la sesión pasada.

**El sistema debía devolver:**

El sistema debía devolver:

Cliente, productos con cantidad y modificaciones, subtotal, costo de domicilio, total, dirección de entrega, medio de pago, tiempo estimado de entrega y si requiere revisión humana.

3\. Consumidor del output

¿Quién necesita leer o utilizar este resultado?

☐ Interfaz

☑ API

☑ Base de datos

☑ Automatización

☑ Otro paso del AI flow

☐ Usuario final

☑ Profesional o revisor humano (cuando requiere\_revision \= true)

**El consumidor principal es**: El sistema de gestión de pedidos (POS/cocina) del restaurante, vía API, y de forma secundaria la persona encargada de logística de domicilios

**Necesita este output para**: Preparar el pedido correctamente en cocina, calcular y cobrar el total exacto, y coordinar la entrega en la dirección indicada

**Necesita este output para:**

4\. Esquema de campos

| Campo | Tipo | Ejemplo | Obligatorio | Valores permitidos | Restricción |
| :---- | :---- | :---- | :---- | :---- | :---- |
| cliente | object | {"nombre":"Juan Pérez","telefono":"+573001234567"} | Sí | — | Debe incluir nombre y teléfono |
| productos | array | \[{"nombre":"Hamburguesa sencilla","cantidad":2,"modificaciones":\["sin cebolla"\],"precio\_unitario":18000}\] | Sí | Solo productos existentes en el menú | No puede estar vacío |
| direccion\_entrega | string | "Cra 45 \#12-30, Barrio X" | Sí | — | Debe estar dentro de la zona de cobertura |
| medio\_pago | string | "nequi" | Sí | efectivo, nequi, daviplata, tarjeta | No acepta otros valores |
| subtotal | number | 36000 | Sí | — | Debe ser igual a la suma de productos x cantidad |
| costo\_domicilio | number | 5000 | Sí | — | Definido según la zona de cobertura |
| total | number | 41000 | Sí | — | Debe ser igual a subtotal \+ costo\_domicilio |
| requiere\_revision | boolean | false | Sí | true / false | true si hay ambigüedad, producto inexistente o dato faltante |

**5\. Decisiones de diseño**

¿Qué campos son obligatorios?: cliente, productos, direccion\_entrega, medio\_pago, subtotal, costo\_domicilio, total y requiere\_revision

¿Qué campos pueden ser opcionales?: Un campo adicional "notas\_cliente" (instrucciones extra como "tocar el timbre 2") puede ser opcional

¿Qué campos pueden usar null?: "telefono" dentro de cliente puede ser null si WhatsApp no expone el número; "costo\_domicilio" puede ser null si aún no se ha calculado la zona

¿Qué campos deberían usar valores permitidos?: medio\_pago (lista cerrada de medios aceptados) y, si se agrega, estado\_pedido (ej. recibido, en\_preparacion, en\_camino, entregado)

¿Qué arrays pueden estar vacíos?: "modificaciones" dentro de cada producto puede ser un array vacío si el cliente no pidió cambios; "productos" nunca puede estar vacío

¿Qué números tienen límites mínimos o máximos?: "cantidad" de cada producto debe ser mayor a 0; "subtotal", "costo\_domicilio" y "total" deben ser mayores o iguales a 0

¿Qué dato no debería inventar la IA?: El nombre exacto de un producto que no está en el menú, su precio, o una dirección que el cliente no escribió; ese tipo de dato siempre debe validarse contra el menú/las zonas reales o marcarse como faltante (null) con requiere\_revision \= true

**6\. JSON de ejemplo**

{  
  "cliente": {  
    "nombre": "Juan Pérez",  
    "telefono": "+573001234567"  
  },  
  "productos": \[  
    {  
      "nombre": "Hamburguesa sencilla",  
      "cantidad": 2,  
      "modificaciones": \["sin cebolla"\],  
      "precio\_unitario": 18000  
    },  
    {  
      "nombre": "Limonada grande",  
      "cantidad": 1,  
      "modificaciones": \[\],  
      "precio\_unitario": 8000  
    }  
  \],  
  "direccion\_entrega": "Cra 45 \#12-30, Barrio X",  
  "medio\_pago": "nequi",  
  "subtotal": 44000,  
  "costo\_domicilio": 5000,  
  "total": 49000,  
  "requiere\_revision": false  
}

**7\. Prompt estructurado**

Actúa como componente de análisis dentro de un producto AI-native.

Tu respuesta será consumida por software.

Devuelve únicamente JSON válido.  
No incluyas explicaciones.  
No uses markdown.  
No agregues texto fuera del JSON.  
No agregues campos no definidos.  
No inventes datos ausentes.  
Usa null cuando un dato no esté disponible.

Estructura requerida:

Actúa como el componente de extracción de pedidos dentro de PedidoBot, un agente de WhatsApp para un restaurante.  
   
Tu respuesta será consumida por software (API del sistema de pedidos).  
   
Devuelve únicamente JSON válido.  
No incluyas explicaciones.  
No uses markdown.  
No agregues texto fuera del JSON.  
No agregues campos no definidos.  
No inventes productos, precios ni direcciones que el cliente no haya escrito.  
Usa null cuando un dato no esté disponible y marca requiere\_revision en true.  
   
Estructura requerida:  
   
{  
  "cliente": { "nombre": "string", "telefono": "string o null" },  
  "productos": \[ { "nombre": "string, debe existir en el menú", "cantidad": "number \> 0",   "modificaciones": "array de strings", "precio\_unitario": "number, tomado del menú" } \],  
  "direccion\_entrega": "string o null",  
  "medio\_pago": "string",  
  "subtotal": "number",  
  "costo\_domicilio": "number o null",  
  "total": "number",  
  "requiere\_revision": "boolean"  
}  
   
Valores permitidos:  
\- medio\_pago: efectivo | nequi | daviplata | tarjeta  
   
Contexto (menú vigente, zonas de cobertura):  
{{MENU\_Y\_ZONAS}}  
   
Input:  
{{INPUT\_REAL}}

**8\. Prueba normal**

**Input**: "Hola buenas\! Quiero 2 hamburguesas sencillas sin cebolla y una limonada grande, para la Cra 45 \#12-30, pago con Nequi"

**Output generado**: El JSON de ejemplo de la sección 6, con requiere\_revision en false

¿El JSON fue válido?: Sí

¿Los campos fueron correctos?: Sí

¿El resultado tuvo sentido?: Sí

**9\. Edge case**

☑ Incompleto

☐ Contradictorio

☑ Ambiguo

☑ Sin datos suficientes

☐ Con información innecesaria

**Input difícil**: "Hola me regalas la de siempre porfa, ah y una gaseosa" (no especifica dirección ni medio de pago, y "la de siempre" no existe como producto en el menú)

**Output generado**: productos: \[{"nombre": null, "cantidad": 1, "modificaciones": \[\], "precio\_unitario": null}, {"nombre": "Gaseosa", "cantidad": 1, "modificaciones": \[\], "precio\_unitario": 4000}\], direccion\_entrega: null, medio\_pago: null, requiere\_revision: true

**10\. Error encontrado**

☐ Campo ausente

☑ Campo inventado

☐ Número como texto

☐ Boolean incorrecto

☐ Valor no permitido

☐ Texto fuera del JSON

☐ null incorrecto

☐ Error lógico

☑ Dato inventado

☐ Otro

**Error encontrado**: En una primera prueba, ante "la de siempre" el modelo inventó el nombre "Hamburguesa sencilla" y su precio, en lugar de dejar el campo en null y marcar requiere\_revision en true

**11\. Ajuste realizado**

☑ El prompt

☐ Los campos

☐ Los tipos

☐ Los valores permitidos

☑ Las restricciones

☐ La validación

☐ El AI flow

**Ajuste realizado**: Se agregó al prompt la instrucción explícita "No inventes productos, precios ni direcciones que el cliente no haya escrito" y se reforzó que, ante cualquier referencia ambigua a un producto, el campo debe quedar en null y requiere\_revision debe ser true en vez de completarse con un supuesto

**12\. Validación humana**

**¿Qué decisión no debería tomar automáticamente la IA?:** Confirmar y enviar a cocina un pedido con un producto que no coincide con el menú, con dirección fuera de la zona de cobertura, o con datos faltantes (dirección, medio de pago)

**¿Cuándo debe intervenir una persona?:** Cuando requiere\_revision sea true: producto ambiguo o inexistente, dirección incompleta o fuera de cobertura, medio de pago no reconocido, o cuando el total calculado no cuadre con la suma de los productos

**¿Qué campo indica que se necesita revisión humana?:** requiere\_revision (boolean)

**13\. Contrato final**

**El equipo entrega:**

☑ Nombre del output: pedido\_whatsapp

☑ Consumidor: API del sistema de pedidos (POS/cocina) del restaurante

☑ Tabla de campos: cliente, productos, direccion\_entrega, medio\_pago, subtotal, costo\_domicilio, total, requiere\_revision

☑ Tipos: object, array, string, string, number, number, number, boolean

☑ Campos obligatorios: todos los anteriores

☑ Campos opcionales: notas\_cliente

☑ Valores permitidos: medio\_pago (efectivo, nequi, daviplata, tarjeta)

☑ Restricciones: productos solo del menú vigente; total \= subtotal \+ costo\_domicilio; cantidad \> 0

☑ JSON válido: ver sección 6

☑ Prompt final: ver sección 7

☑ Input normal: ver sección 8

☑ Edge case: ver sección 9

☑ Error encontrado: ver sección 10

☑ Ajuste realizado: ver sección 11

