<?php
// این فایل برای اجرای سرور PHP در Replit استفاده می‌شود
$host = '0.0.0.0';
$port = 5000;

echo "Starting PHP built-in server on http://$host:$port\n";
echo "Press Ctrl+C to stop the server.\n\n";

$command = "php -S $host:$port";
system($command);
?>