var windowProxy;
		window.onload=function(){ 
			
			// the server sets parentUrl in the page it serves, based on the http-referer
			var windowProxy = new Porthole.WindowProxy(window.parentUrl + "/proxy/");
	 
			function send(data) {
				windowProxy.post(JSON.stringify(data));
			}
			
			windowProxy.addEventListener(function(event) {
				var data = $.parseJSON(event.data),
				requestId = data.requestId,
				params = data.params;
				console.log(event);
				$.ajax(params)
					.done(function(data, textStatus, jqXHR) {
						send({
							type: 'response',
							requestId: requestId,
							success: true,
							data: data,
							textStatus: textStatus
						});
					})
					.fail(function(jqXHR, textStatus, errorThrown) {
						send({
							type: 'response',
							requestId: requestId,
							success: false,
							textStatus: textStatus
						});
					});
			});
			send({type: 'ready'});
		};