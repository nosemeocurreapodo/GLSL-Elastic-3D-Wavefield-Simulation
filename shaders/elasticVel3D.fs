#version 330 core
layout(location = 0) out float upVelx;
layout(location = 1) out float upVely;
layout(location = 2) out float upVelz;

in vec2 g_TexCoords;
flat in int g_layer;

// texture samplers
uniform sampler3D sigmaxxTex;
uniform sampler3D sigmaxyTex;
uniform sampler3D sigmaxzTex;
uniform sampler3D sigmayyTex;
uniform sampler3D sigmayzTex;
uniform sampler3D sigmazzTex;

uniform sampler3D rhoTex;

uniform sampler3D fxTex;
uniform sampler3D fyTex;
uniform sampler3D fzTex;

uniform sampler2D surfaceTex;

uniform float dx;
uniform float dy;
uniform float dz;
uniform float dt;

uniform float ox;
uniform float oy;
uniform float oz;

uniform int layer;

void main()
{
    vec3 Coords3D;
        if(layer < 0)
	  	Coords3D = vec3(gl_FragCoord.xy, g_layer+0.5);
	else
	  	Coords3D = vec3(gl_FragCoord.xy, layer+0.5);
	
	//vec3 TexCoords3D = vec3(Coords3D.x*ox, Coords3D.y*oy, Coords3D.z*oz);
	vec3 TexCoords3D = vec3(g_TexCoords.xy, Coords3D.z*oz);
	
	float c1xy = 9.0/8.0;
    float c2xy = -1.0/24.0;
	
	float c1z = 9.0/8.0;
	float c2z = -1.0/24.0;
	    
	float rhox = texture(rhoTex, TexCoords3D + vec3(0.5*ox,0.0,0.0)).x;
	float rhoy = texture(rhoTex, TexCoords3D + vec3(0.0,0.5*oy,0.0)).x;
	float rhoz = texture(rhoTex, TexCoords3D + vec3(0.0,0.0,0.5*oz)).x;
	
	float surface = texture(surfaceTex, TexCoords3D.xy).x;
	
	if(TexCoords3D.z < surface)
	{
	    //float dist = TexCoords3D.z - surface;
		//float surfaceDamp = pow(1.0*oz,2.0);
		float damp = 0.0;//exp(dist/surfaceDamp);
		rhox = max(rhox*damp,500.0);
		rhoy = max(rhoy*damp,500.0);
		rhoz = max(rhoz*damp,500.0);
	}
	
	
	/*
	float surfacex = texture(surfaceTex, TexCoords3D.xy + vec2(0.5*ox,0.0)).x;
	float surfacey = texture(surfaceTex, TexCoords3D.xy + vec2(0.0,0.5*oy)).x;
	float surfacez = texture(surfaceTex, TexCoords3D.xy + vec2(0.0,   0.0)).x - 0.5*oz;
	
	float surfaceDamp = pow(0.5*oz,2.0);
	float minRho = 100.0;
	
	if(TexCoords3D.z < surfacex)
	{	  
	  float dist = TexCoords3D.z - surfacex;
	  float damp = exp(dist/surfaceDamp);
	  rhox = max(rhox*damp,minRho);
	}
	
    if(TexCoords3D.z < surfacey)
	{	  
	  float dist = TexCoords3D.z - surfacey;
	  float damp = exp(dist/surfaceDamp);
	  rhoy = max(rhoy*damp,minRho);
	}

    if(TexCoords3D.z < surfacez)
	{	  
	  float dist = TexCoords3D.z - surfacez;
	  float damp = exp(dist/surfaceDamp);
	  rhoz = max(rhoz*damp,minRho);
	}	
	*/
	
	//if(TexCoords3D.z < surface + 2.0*oz)
	{
	    c1xy = 1.0;
		c2xy = 0.0;
		c1z = 1.0;
		c2z = 0.0;
	}
    
	
	float d_sigmaxx_dx = c1xy*(texture(sigmaxxTex,TexCoords3D+vec3( ox,0,0)).x - texture(sigmaxxTex,TexCoords3D+vec3( 0,0,0)).x);
	//d_sigmaxx_dx +=  c2xy*(texture(sigmaxxTex,TexCoords3D+vec3( 2*ox,0,0)).x - texture(sigmaxxTex,TexCoords3D+vec3(-ox,0,0)).x);
	d_sigmaxx_dx /= dx;
	
	float d_sigmaxy_dy = c1xy*(texture(sigmaxyTex,TexCoords3D+vec3(0, 0,0)).x - texture(sigmaxyTex,TexCoords3D+vec3(0,-oy,0)).x);
	//d_sigmaxy_dy +=  c2xy*(texture(sigmaxyTex,TexCoords3D+vec3(0, oy,0)).x - texture(sigmaxyTex,TexCoords3D+vec3(0,-2*oy,0)).x);
	d_sigmaxy_dy /= dy;
	
	float d_sigmaxz_dz = c1z*(texture(sigmaxzTex,TexCoords3D+vec3(0,0, 0)).x - texture(sigmaxzTex,TexCoords3D+vec3(0,0,-oz)).x);
	//d_sigmaxz_dz +=  c2z*(texture(sigmaxzTex,TexCoords3D+vec3(0,0, oz)).x - texture(sigmaxzTex,TexCoords3D+vec3(0,0,-2*oz)).x);
	d_sigmaxz_dz /= dz;
	 		  
	float d_sigmaxy_dx = c1xy*(texture(sigmaxyTex,TexCoords3D+vec3( 0,0,0)).x - texture(sigmaxyTex,TexCoords3D+vec3(-ox,0,0)).x);
	//d_sigmaxy_dx +=  c2xy*(texture(sigmaxyTex,TexCoords3D+vec3( ox,0,0)).x - texture(sigmaxyTex,TexCoords3D+vec3(-2*ox,0,0)).x);
	d_sigmaxy_dx /= dx;
	
	float d_sigmayy_dy = c1xy*(texture(sigmayyTex,TexCoords3D+vec3(0, oy,0)).x - texture(sigmayyTex,TexCoords3D+vec3(0, 0,0)).x);
	//d_sigmayy_dy +=  c2xy*(texture(sigmayyTex,TexCoords3D+vec3(0, 2*oy,0)).x - texture(sigmayyTex,TexCoords3D+vec3(0,-oy,0)).x);
	d_sigmayy_dy /= dy;
	
	float d_sigmayz_dz = c1z*(texture(sigmayzTex,TexCoords3D+vec3(0,0, 0)).x - texture(sigmayzTex,TexCoords3D+vec3(0,0,-oz)).x);
	//d_sigmayz_dz +=  c2z*(texture(sigmayzTex,TexCoords3D+vec3(0,0, oz)).x - texture(sigmayzTex,TexCoords3D+vec3(0,0,-2*oz)).x);
	d_sigmayz_dz /= dz;
		  
	float d_sigmaxz_dx = c1xy*(texture(sigmaxzTex,TexCoords3D+vec3( 0,0,0)).x - texture(sigmaxzTex,TexCoords3D+vec3(-ox,0,0)).x);
	//d_sigmaxz_dx +=  c2xy*(texture(sigmaxzTex,TexCoords3D+vec3( ox,0,0)).x - texture(sigmaxzTex,TexCoords3D+vec3(-2*ox,0,0)).x);
	d_sigmaxz_dx /= dx;
	
	float d_sigmayz_dy = c1xy*(texture(sigmayzTex,TexCoords3D+vec3(0, 0,0)).x - texture(sigmayzTex,TexCoords3D+vec3(0,-oy,0)).x);
	//d_sigmayz_dy +=  c2xy*(texture(sigmayzTex,TexCoords3D+vec3(0, oy,0)).x - texture(sigmayzTex,TexCoords3D+vec3(0,-2*oy,0)).x);
	d_sigmayz_dy /= dy;
	
	float d_sigmazz_dz = c1z*(texture(sigmazzTex,TexCoords3D+vec3(0,0, oz)).x - texture(sigmazzTex,TexCoords3D+vec3(0,0, 0)).x);
	//d_sigmazz_dz +=  c2z*(texture(sigmazzTex,TexCoords3D+vec3(0,0, 2*oz)).x - texture(sigmazzTex,TexCoords3D+vec3(0,0,-oz)).x);
	d_sigmazz_dz /= dz;

	upVelx = (d_sigmaxx_dx+d_sigmaxy_dy+d_sigmaxz_dz + texelFetch(fxTex,ivec3(Coords3D),0).x)*dt/rhox;
	upVely = (d_sigmaxy_dx+d_sigmayy_dy+d_sigmayz_dz + texelFetch(fyTex,ivec3(Coords3D),0).x)*dt/rhoy;	
	upVelz = (d_sigmaxz_dx+d_sigmayz_dy+d_sigmazz_dz + texelFetch(fzTex,ivec3(Coords3D),0).x)*dt/rhoz;
}
