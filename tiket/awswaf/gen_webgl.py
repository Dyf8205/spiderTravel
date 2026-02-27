import json
import random
import hashlib


# 真实显卡数据池：厂商、型号、Device ID、平台
GPU_POOL = [
    # ===== NVIDIA Desktop =====
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 4090", "id": "0x00002684", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 4080", "id": "0x00002704", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 4070 Ti", "id": "0x00002782", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 4060 Ti", "id": "0x00002803", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 3090", "id": "0x00002204", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 3080", "id": "0x00002206", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 3070", "id": "0x00002484", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 3060", "id": "0x00002503", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 2080 Ti", "id": "0x00001E04", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 2070 SUPER", "id": "0x00001E84", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 2060", "id": "0x00001F08", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce GTX 1660 SUPER", "id": "0x000021C4", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 16384, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce GTX 1650", "id": "0x00001F82", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 16384, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce GTX 1080 Ti", "id": "0x00001B06", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 16384, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce GTX 1070", "id": "0x00001B81", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 16384, "max_tex": 16384, "max_rb": 4096},
    # ===== NVIDIA Laptop =====
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 4060 Laptop GPU", "id": "0x000028A0", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 3060 Laptop GPU", "id": "0x00002520", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "NVIDIA", "name": "NVIDIA GeForce RTX 3050 Laptop GPU", "id": "0x000025A0", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    # ===== AMD Desktop =====
    {"vendor": "AMD", "name": "AMD Radeon RX 7900 XTX", "id": "0x0000744C", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "AMD", "name": "AMD Radeon RX 7800 XT", "id": "0x00007480", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "AMD", "name": "AMD Radeon RX 6800 XT", "id": "0x000073BF", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "AMD", "name": "AMD Radeon RX 6700 XT", "id": "0x000073DF", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "AMD", "name": "AMD Radeon RX 6600 XT", "id": "0x000073FF", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "AMD", "name": "AMD Radeon RX 580", "id": "0x000067DF", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 16384, "max_tex": 16384, "max_rb": 4096},
    # ===== AMD 集显 =====
    {"vendor": "AMD", "name": "AMD Radeon(TM) Graphics", "id": "0x00001681", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "AMD", "name": "AMD Radeon(TM) 780M Graphics", "id": "0x000015BF", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "AMD", "name": "AMD Radeon(TM) 680M", "id": "0x00001900", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    # ===== Intel 集显 =====
    {"vendor": "Intel", "name": "Intel(R) Iris(R) Xe Graphics", "id": "0x00009A49", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "Intel", "name": "Intel(R) Iris(R) Xe Graphics", "id": "0x000046A6", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "Intel", "name": "Intel(R) UHD Graphics 770", "id": "0x00004680", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "Intel", "name": "Intel(R) UHD Graphics 730", "id": "0x00004692", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "Intel", "name": "Intel(R) UHD Graphics 630", "id": "0x00003E92", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 16384, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "Intel", "name": "Intel(R) HD Graphics 620", "id": "0x00005916", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 16384, "max_tex": 16384, "max_rb": 4096},
    {"vendor": "Intel", "name": "Intel(R) Arc(TM) A770 Graphics", "id": "0x000056A1", "api": "Direct3D11 vs_5_0 ps_5_0, D3D11", "point_size": 1024, "viewport": 32767, "max_tex": 16384, "max_rb": 4096},
    # ===== Apple (macOS) =====
    {"vendor": "Apple", "name": "Apple M1", "id": None, "api": "Metal", "point_size": 511, "viewport": 16384, "max_tex": 16384, "max_rb": 1024, "platform": "mac"},
    {"vendor": "Apple", "name": "Apple M1 Pro", "id": None, "api": "Metal", "point_size": 511, "viewport": 16384, "max_tex": 16384, "max_rb": 1024, "platform": "mac"},
    {"vendor": "Apple", "name": "Apple M1 Max", "id": None, "api": "Metal", "point_size": 511, "viewport": 16384, "max_tex": 16384, "max_rb": 1024, "platform": "mac"},
    {"vendor": "Apple", "name": "Apple M2", "id": None, "api": "Metal", "point_size": 511, "viewport": 16384, "max_tex": 16384, "max_rb": 1024, "platform": "mac"},
    {"vendor": "Apple", "name": "Apple M2 Pro", "id": None, "api": "Metal", "point_size": 511, "viewport": 16384, "max_tex": 16384, "max_rb": 1024, "platform": "mac"},
    {"vendor": "Apple", "name": "Apple M2 Max", "id": None, "api": "Metal", "point_size": 511, "viewport": 16384, "max_tex": 16384, "max_rb": 1024, "platform": "mac"},
    {"vendor": "Apple", "name": "Apple M3", "id": None, "api": "Metal", "point_size": 511, "viewport": 16384, "max_tex": 16384, "max_rb": 1024, "platform": "mac"},
    {"vendor": "Apple", "name": "Apple M3 Pro", "id": None, "api": "Metal", "point_size": 511, "viewport": 16384, "max_tex": 16384, "max_rb": 1024, "platform": "mac"},
    {"vendor": "Apple", "name": "Apple M4", "id": None, "api": "Metal", "point_size": 511, "viewport": 16384, "max_tex": 16384, "max_rb": 1024, "platform": "mac"},
]

# Windows (D3D11) 的扩展
EXTENSIONS_WINDOWS = "ANGLE_instanced_arrays;EXT_blend_minmax;EXT_clip_control;EXT_color_buffer_half_float;EXT_depth_clamp;EXT_disjoint_timer_query;EXT_float_blend;EXT_frag_depth;EXT_polygon_offset_clamp;EXT_shader_texture_lod;EXT_texture_compression_bptc;EXT_texture_compression_rgtc;EXT_texture_filter_anisotropic;EXT_texture_mirror_clamp_to_edge;EXT_sRGB;KHR_parallel_shader_compile;OES_element_index_uint;OES_fbo_render_mipmap;OES_standard_derivatives;OES_texture_float;OES_texture_float_linear;OES_texture_half_float;OES_texture_half_float_linear;OES_vertex_array_object;WEBGL_blend_func_extended;WEBGL_color_buffer_float;WEBGL_compressed_texture_s3tc;WEBGL_compressed_texture_s3tc_srgb;WEBGL_debug_renderer_info;WEBGL_debug_shaders;WEBGL_depth_texture;WEBGL_draw_buffers;WEBGL_lose_context;WEBGL_multi_draw;WEBGL_polygon_mode"

# macOS (Metal) 的扩展 - 多了 ASTC/ETC/PVRTC
EXTENSIONS_MAC = "ANGLE_instanced_arrays;EXT_blend_minmax;EXT_clip_control;EXT_color_buffer_half_float;EXT_depth_clamp;EXT_disjoint_timer_query;EXT_float_blend;EXT_frag_depth;EXT_polygon_offset_clamp;EXT_shader_texture_lod;EXT_texture_compression_bptc;EXT_texture_compression_rgtc;EXT_texture_filter_anisotropic;EXT_texture_mirror_clamp_to_edge;EXT_sRGB;KHR_parallel_shader_compile;OES_element_index_uint;OES_fbo_render_mipmap;OES_standard_derivatives;OES_texture_float;OES_texture_float_linear;OES_texture_half_float;OES_texture_half_float_linear;OES_vertex_array_object;WEBGL_blend_func_extended;WEBGL_color_buffer_float;WEBGL_compressed_texture_astc;WEBGL_compressed_texture_etc;WEBGL_compressed_texture_etc1;WEBGL_compressed_texture_pvrtc;WEBGL_compressed_texture_s3tc;WEBGL_compressed_texture_s3tc_srgb;WEBGL_debug_renderer_info;WEBGL_debug_shaders;WEBGL_depth_texture;WEBGL_draw_buffers;WEBGL_lose_context;WEBGL_multi_draw;WEBGL_polygon_mode"


def _md5(s):
    return hashlib.md5(s.encode()).hexdigest()


def _rand_hash(seed_str):
    return _md5(seed_str + str(random.random()))


def build_unmasked_renderer(gpu):
    """构建 ANGLE 格式的 unmasked_renderer"""
    if gpu.get("platform") == "mac":
        return f"ANGLE (Apple, ANGLE Metal Renderer: {gpu['name']}, Unspecified Version)"
    else:
        return f"ANGLE ({gpu['vendor']}, {gpu['name']} ({gpu['id']}) {gpu['api']})"


def get_random_webgl():
    gpu = random.choice(GPU_POOL)
    is_mac = gpu.get("platform") == "mac"

    extensions = EXTENSIONS_MAC if is_mac else EXTENSIONS_WINDOWS
    unmasked_renderer = build_unmasked_renderer(gpu)
    unmasked_vendor = "Google Inc. (Apple)" if is_mac else f"Google Inc. ({gpu['vendor']})"

    vp = gpu["viewport"]
    max_rb = gpu["max_rb"]

    webgl_detail = {
        "webgl_extensions": extensions,
        "webgl_extensions_hash": _rand_hash(extensions),
        "webgl_renderer": "WebKit WebGL",
        "webgl_vendor": "WebKit",
        "webgl_version": "WebGL 1.0 (OpenGL ES 2.0 Chromium)",
        "webgl_shading_language_version": "WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)",
        "webgl_aliased_line_width_range": "[1, 1]",
        "webgl_aliased_point_size_range": f"[1, {gpu['point_size']}]",
        "webgl_antialiasing": True,
        "webgl_bits": "8,8,24,8,8,0",
        "webgl_max_params": f"16,32,{gpu['max_tex']},1024,{gpu['max_tex']},16,16,30,16,16,{max_rb}",
        "webgl_max_viewport_dims": f"[{vp}, {vp}]",
        "webgl_unmasked_vendor": unmasked_vendor,
        "webgl_unmasked_renderer": unmasked_renderer,
        "webgl_vsf_params": "23,127,127,23,127,127,23,127,127",
        "webgl_vsi_params": "0,31,30,0,31,30,0,31,30",
        "webgl_fsf_params": "23,127,127,23,127,127,23,127,127",
        "webgl_fsi_params": "0,31,30,0,31,30,0,31,30",
        "webgl_hash_webgl": _rand_hash(unmasked_renderer),
    }
    return {
        "webgl_unmasked_renderer": unmasked_renderer,
        "webgl": [webgl_detail],
    }


if __name__ == "__main__":
    result = get_random_webgl()
    print(json.dumps(result, indent=2, ensure_ascii=False))
