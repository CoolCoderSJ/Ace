/* eslint-env browser, serviceworker, es6 */

'use strict';

self.addEventListener('push', function(event) {

  
  const title = event.data.text().split(" || ")[0];
  const options = {
    body: event.data.text().split(" || ")[1]
  };

  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function(event) {

  event.notification.close();

  event.waitUntil(
    clients.openWindow('https://ace.coolcodersj.repl.co/')
  );
});
