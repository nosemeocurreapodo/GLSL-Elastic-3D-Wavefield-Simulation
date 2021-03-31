#version 330 core
layout (location = 0) in vec4 aPos;

out vec3 v_TexCoords;

uniform mat4 cameraPose;
uniform mat4 projection;

void main()
{
    vec4 pworld = vec4(aPos.xyz,1.0);
    vec4 pcamera = cameraPose * pworld;
    gl_Position = projection * pcamera;
	
	v_TexCoords = (aPos.xyz+vec3(1.0,1.0,1.0))/2.0;
}
