# Luce demos

Small applications written in Luce, using the Luce Base `luce-ui` and `luce-3d`
packages. Native compilation is the default. The standard library owns window,
input and GPU backend resources; applications own their behavior.

- `src/ui_demo.luc`: a counter, a button and declarative stack layout. A retained
  connection calls the counter's bound `increment` method.
- `src/sphere.luc`: a lit sphere and orbiting moon inside luce-ui's `SceneView`, with
  pause/resume and reset controls. `Application.on_frame` drives animation.

Check out `luce-base`, `luce`, `luce-ui`, `luce-3d` and what they use alongside this
repository, at main (`python3 ../luce-base/tools/checkout_main.py . ../luce` clones the
missing ones). Build the compilers, then:

```sh
./build.sh
./build/ui
./build/sphere
```

Running the examples requires macOS with Metal. Their portable application and
package code also compiles on Linux; native Vulkan presentation is future work.
The `--smoke` argument closes each window after twelve frames.

`./build.sh` leaves just `build/ui` and `build/sphere`. To choose an optimization
level or output directory, use `python3 tools/build.py --opt 3 --output-directory
/path/to/output`. Dependencies are resolved through their manifests and public
exports. Normal builds keep no generated Base source or staged dependencies.

`luc test` runs `tests/interaction`, the counter/pause/reset/animation handlers
driven without a window, and `tests/builds`, which compiles both examples and checks
that successful and failed builds leave nothing in the temporary directory. To see the
windows themselves, run `build/ui --smoke` and `build/sphere --smoke` after `./build.sh`
(with `MTL_DEBUG_LAYER=1 MTL_SHADER_VALIDATION=1` for Metal's validation on macOS).

The examples intentionally retain the language's current explicit `try` syntax.
Error-handling ergonomics are a separate language design discussion, not a
package-level exception suppression policy.

These are development examples with no compatibility promise before the first
release. Licensed under MIT or Apache-2.0, at your option.

## Windows x64

Run `luc test` as on the other hosts.
For real windows and rendering, install the Vulkan SDK and start a fresh terminal with `VULKAN_SDK` set. Run `python tools/build.py`, then `build/ui.exe --smoke` or `build/sphere.exe --smoke`; they need an interactive desktop and Vulkan hardware.
