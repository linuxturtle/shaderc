// Copyright 2015 The Shaderc Authors. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Some of the tests here check code paths that are not checked by
// integration tests.
// Generally, these would be conditions not generated by the Glslang
// compiler.  It's easier to write these unit tests than to inject
// a dependency on a fake compiler.

#include <sstream>

#include <gtest/gtest.h>
#include "shaderc/shaderc.h"

#include "shader_stage.h"

using shaderc_util::string_piece;

namespace {

TEST(DeduceDefaultShaderKindFromFileName, ValidStage) {
  std::stringstream error_stream;
  EXPECT_EQ(shaderc_glsl_default_vertex_shader,
            glslc::DeduceDefaultShaderKindFromFileName("a.vert"));

  EXPECT_EQ(shaderc_glsl_default_fragment_shader,
            glslc::DeduceDefaultShaderKindFromFileName("a.frag"));

  EXPECT_EQ(shaderc_glsl_default_geometry_shader,
            glslc::DeduceDefaultShaderKindFromFileName("a.geom"));

  EXPECT_EQ(shaderc_glsl_default_tess_control_shader,
            glslc::DeduceDefaultShaderKindFromFileName("a.tesc"));

  EXPECT_EQ(shaderc_glsl_default_tess_evaluation_shader,
            glslc::DeduceDefaultShaderKindFromFileName("a.tese"));

  EXPECT_EQ(shaderc_glsl_default_compute_shader,
            glslc::DeduceDefaultShaderKindFromFileName("a.comp"));
}

TEST(DeduceDefaultShaderKindFromFileName, InvalidStage) {
  std::stringstream error_stream;
  EXPECT_EQ(shaderc_glsl_infer_from_source,
            glslc::DeduceDefaultShaderKindFromFileName("a.glsl"));

  EXPECT_EQ(shaderc_glsl_infer_from_source,
            glslc::DeduceDefaultShaderKindFromFileName("-"));

  EXPECT_EQ(shaderc_glsl_infer_from_source,
            glslc::DeduceDefaultShaderKindFromFileName("a.foo"));

  EXPECT_EQ(shaderc_glsl_infer_from_source,
            glslc::DeduceDefaultShaderKindFromFileName("no-file-extension"));
}

}  // anonymous namespace
