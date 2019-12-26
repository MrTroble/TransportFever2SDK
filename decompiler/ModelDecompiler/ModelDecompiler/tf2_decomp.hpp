#pragma once

#include <tiny_gltf.h>
#include <lua.hpp>
#include <regex>

namespace tf2decomp {

	using namespace tinygltf;

	// Error codes
	// -1. couldn't open file
	// Positiver error code is a lua error (see LUA_OK)

	std::string readfile(const char* file, int* result) {
		FILE* fileptr = nullptr;
		errno_t lastresult = fopen_s(&fileptr, file, "r");
		if (fileptr == nullptr || lastresult != 0) {
			*result = -1;
			return "";
		}
		fseek(fileptr, 0, SEEK_END);
		uint64_t length = ftell(fileptr);
		fseek(fileptr, 0, SEEK_SET);
		std::string str;
		str.resize(length);
		fread(&str[0], 1, length, fileptr);
		return str;
	}


#ifdef DEBUG 
#define CHECK(imp) luaresult = imp;\
	if (luaresult != LUA_OK) {\
		*result = luaresult;\
        printf("Error in %s line %i", __FILE__, __LINE__);\
		return Model();\
	}
#else
#define CHECK(imp) luaresult = imp;\
	if (luaresult != LUA_OK) {\
		*result = luaresult;\
		return Model();\
	}
#endif  


	Model convertFromMemory(std::string content, int* result) {
		lua_State* l = luaL_newstate();
		luaL_openlibs(l);

		std::regex regex = std::regex("data()");
		content = "dataf = "  + std::regex_replace(content, regex, "");
		printf(content.c_str());

		int CHECK(luaL_loadstring(l, content.c_str()));

		CHECK(lua_getglobal(l, "dataf"))

		printf(lua_typename(l, lua_type(l, -1)));

		CHECK(lua_pcall(l, 0, LUA_MULTRET, 0));


		//CHECK(lua_pcall(l, 0, LUA_MULTRET, 0));

		//lua_setglobal(l, "dat");

		//CHECK(lua_getglobal(l, "dat"));

		printf(lua_typename(l, lua_type(l, -1)));
		lua_close(l);
	}

	Model convertFromFile(const char* file, int* result) {
		std::string content = readfile(file, result);
		if (content.empty())
			return Model();
		return convertFromMemory(content, result);
	}
}
