#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;

//sampler2d para representar datos 2d
uniform sampler2D u_texture_0;
uniform vec3 camPos;

vec3 getLight(vec3 color){
    vec3 Normal = normalize(normal);
    //Luz de ambiente
    vec3 ambient = light.Ia;


    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.Id;

    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * light.Is;

    return color * (ambient + diffuse + specular );
}


void main() 
{
    float gamma = 2.2;
    //toma un color predefinido y lo asigna al atributo de salida fragColor, que se utilizará para determinar 
    //el color final de cada fragmento en la pantalla.
    //vec3 color = vec3(uv_0, 0);  // Rojo
    vec3 color = texture(u_texture_0, uv_0).rgb;
    
    color = pow(color, vec3(gamma));
    
    color = getLight(color);
    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0); // Asigna el color al fragmento
}
