#version 330 core
layout(location = 0) out float savedData;

uniform sampler3D velxTex;
uniform sampler3D velyTex;
uniform sampler3D velzTex;
uniform sampler3D sigmaxxTex;
uniform sampler3D sigmaxyTex;
uniform sampler3D sigmaxzTex;
uniform sampler3D sigmayyTex;
uniform sampler3D sigmayzTex;
uniform sampler3D sigmazzTex;

uniform vec3 recieverLoc[20];

uniform int t_step;

void main()
{
    if(gl_FragCoord.y == t_step+0.5)
	{
	  for(int i = 0; i < 20; i++)
	  {
		float surface = recieverLoc[i].z;
		//float surface = 0.125+oz*0.5;
		float x = recieverLoc[i].x;
		float y = recieverLoc[i].y;
		
		int offset = 9*i;
		
		if(int(gl_FragCoord.x) == 0 + offset)  
			savedData = texture(velxTex, vec3(x,y,surface)).x;
		if(int(gl_FragCoord.x) == 1 + offset) 
			savedData = texture(velyTex, vec3(x,y,surface)).x;
		if(int(gl_FragCoord.x) == 2 + offset) 
			savedData = texture(velzTex, vec3(x,y,surface)).x;
		if(int(gl_FragCoord.x) == 3 + offset)  
			savedData = texture(sigmaxxTex, vec3(x,y,surface)).x;
		if(int(gl_FragCoord.x) == 4 + offset) 
			savedData = texture(sigmaxyTex, vec3(x,y,surface)).x;
		if(int(gl_FragCoord.x) == 5 + offset) 
			savedData = texture(sigmaxzTex, vec3(x,y,surface)).x;
		if(int(gl_FragCoord.x) == 6 + offset)  
			savedData = texture(sigmayyTex, vec3(x,y,surface)).x;
		if(int(gl_FragCoord.x) == 7 + offset) 
			savedData = texture(sigmayzTex, vec3(x,y,surface)).x;
		if(int(gl_FragCoord.x) == 8 + offset) 
			savedData = texture(sigmazzTex, vec3(x,y,surface)).x;
	    
	  }
	}
	else
	{
	  discard;
	}
}
