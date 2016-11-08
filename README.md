# SQUAD - Software Quality Dashboard

## Data model

```
+----+  * +-------+  * +-----+  * +-------+  * +----+ *   1 +-----+
|Team|--->|Project|--->|Build|--->|TestRun|--->|Test|------>|Suite|
+----+    +-------+    +-----+    +-------+    +----+       +-----+
                                    | *   |                    ^ 1
                                    |     |  * +------+ *      |
                                    |     +--->|Metric|--------+
                                    |          +------+
                                    v 1
                                  +-----------+
                                  |Environment|
                                  +-----------+
```

SQUAD is multi-team and multi-project. Each team can have multiple projects.
For each project, you can have multiple builds, and for each build, multiple
test runs. Each test run can include multiple test results, which can be either
pass/fail results, or metrics, containing one or more measurement
values. Test and metric results can belong to a Suite, which is a basically
used to group and analyze results together. Every test suite must be associated
with exactly one Environment, which describes the environment in which the
tests were executed, such as hardware platform, hardware configuration, OS,
build settings (e.g. regular compilers vcs optimized compilers), etc. Results
are always organized by environments, so we can compare apples to apples.

## Submitting results

The API is the following

**POST** /api/submit/:team/:project/:build/:environment

* `:team` is the team identifier. It must exist previously
* `:project` is the project identifier. It will be craeted a automatically if
  it does not exist previously.
* `:build` is the build identifier. It can be a git commit hash, a Android
  manifest hash, or anything really. Extra information on the build can be
  submitted as an attachment. If a build timestamp is not informed there, the
  time of submission is assumed.
* `:environment` is the environmenr identitifer. It will be created
  automatically if does not exist before.

The test data must be submitted as file attachments in the `POST` request. The
following files are supported:

* `tests`: test results data
* `metrics`: metrics data

See [Input file formats](#input-file-formats) below for details on the format
of these data files.

Example:

```
$ curl \
    --header "Auth-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
    --form tests=@/path/to/test-rsults.json \
    --form metrics=@/path/to/metrics.json \
    https://squad.example.com/api/submit/my-team/my-project/x.y.z/my-ci-env
```

Since test results should always come from automation systems, the API is the
only way to submit results into the system. Even manual testing should be
automated with a driver program that asks for user input, and them at the end
prepares all the data in a consistent way, and submits it to dashboard.

## Input file formats

### Test results

Test results must be posted as JSON, encoded in UTF-8. The JSON data must be a
hash (an object, strictly speaking). Test names go in the keys, and values must
be either `"pass"` or `"fail"`.

Tests can be grouped in suites. For that, the test name must be prefixed with
the group name and a slash (`/`). Therefore, slashes are reserved characters in
this context, and cannot be used in test names. Group names can have embedded
slashes in them; so "foo/bar" means group "foo", test "bar"; and "foo/bar/baz"
means group "foo/bar" test "baz".

Example:


```json
{
  "test1": "pass",
  "test2": "pass",
  "group1/test1": "pass",
  "group1/test2": "fail",
  "group1/subgroup/test1": "pass",
  "group1/subgroup/test2": "pass"
}
```

### Metrics

Metrics must be posted as JSON, encoded in UTF-8. The JSON data must be a hash
(an object, strictly speaking). Metric names go in the keys, and values must be
either a single number, or an array of numbers. In the case of an array of
numbers, then their mean will be used as the metric result; the whole set of
results will be used where applicable, e.g. to display ranges.

As with test results, metrics can be grouped in suites. For that, the test name
must be prefixed with the group name and a slash (`/`). Therefore, slashes are
reserved characters in this context, and cannot be used in test names. Group
names can have embedded slashes in them; so "foo/bar" means group "foo", test
"bar"; and "foo/bar/baz" means group "foo/bar" test "baz".

Example:

```json
{
  "v1": 1,
  "v2": 2.5,
  "group1/v1": [1.2, 2.1, 3.03],
  "group1/subgroup/v1": [1, 2, 3, 2, 3, 1]
}
```

## How to support multiple use cases

* Branches: use separate projects, one per branch. e.g. `foo-master` and
  `foo-stable`.
* ...

## License

Copyright © 2016 Linaro Limited

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
