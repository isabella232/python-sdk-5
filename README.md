# ConfigCat SDK for Python
ConfigCat is a cloud based configuration as a service. It integrates with your apps, backends, websites, and other programs, so you can configure them through this website even after they are deployed.
https://configcat.com  

[![Build Status](https://travis-ci.org/configcat/python-sdk.svg?branch=master)](https://travis-ci.org/configcat/python-sdk) 
[![codecov](https://codecov.io/gh/ConfigCat/python-sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/ConfigCat/ConfigCat-Client)
[![PyPI](https://img.shields.io/pypi/v/configcat-client.svg)](https://pypi.python.org/pypi/configcat-client)
[![PyPI](https://img.shields.io/pypi/pyversions/configcat-client.svg)](https://pypi.python.org/pypi/configcat-client)

## Getting started

**1. Install the ConfigCat-Client package with `pip`**

```bash
pip install configcat-client
```

**2. Import `configcatclient` to your application**

```python
import configcatclient
```

**3. Get your Project Secret from the [ConfigCat.com](https://configcat.com) portal**

![YourConnectionUrl](https://raw.githubusercontent.com/configcat/python-sdk/master/media/readme01.png  "YourProjectSecret")

**4. Initialize and get the client**

```python
configcatclient.initialize('<PLACE-YOUR-PROJECT-SECRET-HERE>')
client = configcatclient.get()
```

**5. Get your config value**
```python
isMyAwesomeFeatureEnabled = client.get_value('key-of-my-awesome-feature', False)
if isMyAwesomeFeatureEnabled:
    # show your awesome feature to the world!
```

**6. On application exit:**
```python
configcatclient.stop()
```

## Configuration
Client supports three different caching policies to acquire the configuration from ConfigCat. When the client fetches the latest configuration, puts it into the internal cache and serves any configuration acquisition from cache. With these caching policies you can manage your configurations' lifetimes easily.

### Auto polling (default)
Client downloads the latest configuration and puts into a cache repeatedly. Use ```poll_interval_seconds``` parameter to manage polling interval.
Use ```on_configuration_changed_callback``` parameter to get notification about configuration changes. 
*
### Lazy loading
Client downloads the latest configuration only when it is not present or expired in the cache. 
Use ```cache_time_to_live_seconds``` parameter to manage configuration lifetime.

### Manual polling
With this mode you always have to call ```force_refresh()``` method to fetch the latest configuration into the cache. When the cache is empty (for example after client initialization) and you try to acquire any value you'll get the default value!

---

Initializing the client and the configuration parameters are different for each cache policy:

### Auto polling  
```configcatclient.initialize(...)```

| ParameterName        | Description           | Default  |
| --- | --- | --- |
| ```project_secret```      | Project Secret to access your configuration  | REQUIRED |
| ```poll_interval_seconds ```      | Polling interval|   60 | 
| ```max_init_wait_time_seconds```      | Maximum waiting time between the client initialization and the first config acquisition in secconds.|   5 |
| ```on_configuration_changed_callback```      | Callback to get notification about configuration changes. |   None |
| ```config_cache_class```      | Custom cache implementation class. |   None |

#### Example - increase ```poll_interval_seconds``` to 600 seconds:

```python
configcatclient.initialize('<PLACE-YOUR-PROJECT-SECRET-HERE>', poll_interval_seconds=600)
```

#### Example - get notification about configuration changes via ```on_configuration_changed_callback```:  

```python
def configuration_changed_callback(self):
    # Configuration changed.
    pass
    
configcatclient.initialize('<PLACE-YOUR-PROJECT-SECRET-HERE>', on_configuration_changed_callback=configuration_changed_callback)
```

### Lazy loading
```configcatclient.initialize_lazy_loading(...)```

| ParameterName        | Description           | Default  |
| --- | --- | --- | 
| ```project_secret```      | Project Secret to access your configuration  | REQUIRED |
| ```cache_time_to_live_seconds```      | Use this value to manage the cache's TTL. |   60 |
| ```config_cache_class```      | Custom cache implementation class. |   None |

#### Example - increase ```cache_time_to_live_seconds``` to 600 seconds:

```python
configcatclient.initialize_lazy_loading('<PLACE-YOUR-PROJECT-SECRET-HERE>', cache_time_to_live_seconds=600)
```

#### Example - use a custom ```config_cache_class```:

```python
from configcatclient.interfaces import ConfigCache


class InMemoryConfigCache(ConfigCache):

    def __init__(self):
        self._value = None

    def get(self):
        return self._value

    def set(self, value):
        self._value = value

configcatclient.initialize_lazy_loading('<PLACE-YOUR-PROJECT-SECRET-HERE>', config_cache_class=InMemoryConfigCache)
```

### Manual polling
```configcatclient.initialize_manual_polling(...)```

| ParameterName        | Description           | Default  |
| --- | --- | --- | 
| ```project_secret```      | Project Secret to access your configuration  | REQUIRED |
| ```config_cache_class```      | Custom cache implementation class. |   None |

#### Example - call ```force_refresh()``` to fetch the latest configuration:

```python
configcatclient.initialize_manual_polling('<PLACE-YOUR-PROJECT-SECRET-HERE>')
configcatclient.get().get_value('test_key', 'default_value') # This will return 'default_value' 
configcatclient.get().force_refresh()
configcatclient.get().get_value('test_key', 'default_value') # This will return the real value for key 'test_key'
```

## Members
### Methods
| Name        | Description           |
| :------- | :--- |
| ``` configcatclient.get().get_configuration_json() ``` | Returns configuration as a json dictionary |
| ``` configcatclient.get().get_value(key, defaultValue) ``` | Returns the value of the key |
| ``` configcatclient.get().force_refresh() ``` | Fetches the latest configuration from the server. You can use this method with WebHooks to ensure up to date configuration values in your application. |

## Logging
The ConfigCat SDK uses the default Python `logging` package for logging.

## Sample projects
* [Console sample](https://github.com/configcat/python-sdk/tree/master/samples/consolesample)
* [Django web app sample](https://github.com/configcat/python-sdk/tree/master/samples/webappsample)