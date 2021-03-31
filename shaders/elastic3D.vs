#version 330 core
layout (location = 0) in vec2 aPos;
layout (location = 1) in vec2 aTexCoords;

out vec2 v_TexCoords;
flat out int v_layer;

uniform int layer;

void main()
{
    gl_Position = vec4(aPos.x, aPos.y, 0.0, 1.0);
    v_TexCoords = aTexCoords;
    //v_layer = layer;
    v_layer = gl_InstanceID;
}
