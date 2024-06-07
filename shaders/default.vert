#version 330 core

//define un atributo de entrada llamado in_position, que espera recibir vectores de 3
// componentes y está asociado con la ubicación de índice 0


layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;

out vec2 uv_0;
out vec3 normal;
out vec3 fragPos;

//dos uniformes de tipo matriz (mat4), m_proj y m_view. Estos uniformes se utilizan 
//para almacenar las matrices de proyección (m_proj) y de vista (m_view) que se 
//proporcionan desde la aplicación principal 
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;


void main() {
    uv_0 = in_texcoord_0;
    fragPos = vec3(m_model * vec4(in_position, 1.0));
    normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);

    // toma las coordenadas del vértice proporcionadas por el atributo de entrada in_position, las 
    //convierte en un vector de coordenadas homogéneas y las asigna a gl_Position
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
    //La posición del vértice en el espacio de recorte
    //aplica las transformaciones de vista y proyección a las coordenadas del vértice, 
    //convirtiéndolas en coordenadas de pantalla 
}
    


