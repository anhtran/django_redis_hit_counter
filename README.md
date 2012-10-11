# django_redis_hit_counter
Simple app for counting hit views

## Usage

### Settings
* Add `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB` to `settings.py` for redis.
* Add `HIT_COUNTER_PERIOD` for counting the same ip address/user agent. Default: `60*30`.

### Templates
* Load tags to your templates: `{% load hit_counter_tags %}`
* Use `hit_counter_js` in page you want to add hit count. For example: `{% hit_counter_js obj }`
* Use `hit_counter` to see the hits. For example: `{% hit_counter obj as hits %}{{ hit }} views`