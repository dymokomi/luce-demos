# Luce demos

Small applications written in Luce, using the Luce Base `luce-ui` and `luce-3d`
packages. Native compilation is the default. The standard library owns window,
input and GPU backend resources; applications own their behavior.

- `src/ui_demo.luc`: a counter, a button and declarative stack layout. A retained
  connection calls the counter's bound `increment` method.
- `src/sphere.luc`: a lit sphere and orbiting moon inside a `SceneView`, with
  pause/resume and reset controls. `Application.on_frame` drives animation.

Check out the exact revisions from `bootstrap/BASE`, `bootstrap/LUCE`,
`bootstrap/UI` and `bootstrap/THREE` alongside this repository as `luce-base`,
`luce`, `luce-ui` and `luce-3d`. Build the compilers, then:

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

`./test.sh` compiles both examples and runs their counter/pause/reset/animation
interaction tests at native optimization levels 0–3. It also checks that successful
and failed builds clean up their temporary output. `./test.sh --gui` additionally
runs both windows with Metal API/shader validation. CI runs portable tests on
ARM64 macOS and x86-64 Linux, with GUI smoke tests on macOS.

The examples intentionally retain the language's current explicit `try` syntax.
Error-handling ergonomics are a separate language design discussion, not a
package-level exception suppression policy.

These are development examples with no compatibility promise before the first
release. Licensed under MIT or Apache-2.0, at your option.
