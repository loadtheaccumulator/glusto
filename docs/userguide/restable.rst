Glusto Simple REST Client
-------------------------

Glusto provides simple methods for basic REST API get, post, put, and delete functionality.

Making REST API Requests
========================

Glusto supports the four basic REST API request types.

* GET
* POST
* PUT
* DELETE

Making a GET Request
~~~~~~~~~~~~~~~~~~~~

To submit a GET request to a url, use the ``rest_get()`` method.

	::

		>>> g.rest_get('http://httpbin.org/get')

Making a POST Request
~~~~~~~~~~~~~~~~~~~~~

To submit a POST request to a url, use the ``rest_post()`` method.

	::

		>>> g.rest_post('http://httpbin.org/post', data={'this': 'yada1', 'that': 'yada2'})


Making a PUT Request
~~~~~~~~~~~~~~~~~~~~

To submit a PUT request to a url, use the ``rest_put()`` method.

	::

		>>> g.rest_put('http://httpbin.org/put', data={'this': 'yada1', 'that': 'yada2'})


Making a DELETE Request
~~~~~~~~~~~~~~~~~~~~~~~

To submit a DELETE request to a url, use the ``rest_delete()`` method.

	::

		>>> g.rest_delete('http://httpbin.org/delete', data={'this': 'yada1', 'that': 'yada2'})

Handling the Request Response
=============================

Glusto provides the return in a tuple similar to the SSH calls in the ``glusto.Connectible`` class.

	::

		>>> g.rest_get('http://192.168.1.112:8081/hello')
		(0, 'HelloWorld from GlusterFS Application', None)

The returned tuple consists of the return code, the response output, and the response error.

.. Note::

	The return code is the standard HTTP code returned by the web server on server response error (e.g., 404), otherwise returns zero for a successful request.

Using the Request Response as Config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The output of the response will be in string format.

If the string is yaml formatted text, it can be converted into a dictionary object
using the ``load_yaml_string()`` method.

	::

		>>> g.rest_get('http://192.168.1.112:8081/clusters')
		(0, '{"clusters":["e2effa75a5a50560c3250b67cf71b465"]}\n', None)
		>>> rcode, rout, rerr = g.rest_get('http://192.168.1.112:8081/clusters')[1]
		>>> config = g.load_yaml_string(rout)
		>>> config
		{'clusters': ['e2effa75a5a50560c3250b67cf71b465']}
		>>> config['clusters']
		['e2effa75a5a50560c3250b67cf71b465']

