self.addEventListener('push', function(event) {
    const data = event.data.json();
    console.log("Push received:", data);
    self.registration.showNotification(data.title, {
        body: data.message,
        icon: '/static/icons/icon-192x192.png',
        data: { url: data.url }
    });
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(
        clients.openWindow(event.notification.data.url)
    );
});