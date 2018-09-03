# NetworkOptimization

Python3 project.

## Configuration

Install required packages from the project root path:

```
pip install -r requirements.txt
```

---
---
## Commands

See  help:

```
python3 NetworkOptimization.py --help
```
Usage:

```
python3 NetworkOptimization.py [OPTIONS] COMMAND [ARGS]

Options:
  --help  Show this message and exit.

Commands:
  test-area
  test-line
  test-model

```

---

1. **test-model**

Tests builted for the network model, such as get fitness, test network layouts, etc.

```
python3 NetworkOptimization.py test-model [OPTIONS]

Options:
  -t, --test TEXT  Select the test you want to run.  [required]
  --help           Show this message and exit.
```

2. **test-line**

Test generation of a line of nodes. You must pass the number of nodes contained in the respective line by the option `-n`.

```
python3 NetworkOptimization.py test-line --help
Usage: NetworkOptimization.py test-line [OPTIONS]

Options:
  -n, --nodes INTEGER  Number of nodes of specified line.  [required]
  --help               Show this message and exit.
```

3. **test-area**

Test generation of an area of nodes. You must pass the number of nodes contained in the respective area by the option `-n`.

```
python3 NetworkOptimization.py test-area --help
Usage: NetworkOptimization.py test-area [OPTIONS]

Options:
  -n, --nodes INTEGER  Number of nodes of specified area.  [required]
  --help               Show this message and exit.
```

