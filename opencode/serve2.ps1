$port = 8080
$dir = "C:\Users\katak\AppData\Local\Temp\opencode"
$ip = "192.168.100.57"
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://$($ip):$port/")
$listener.Prefixes.Add("http://127.0.0.1:$port/")
$listener.Start()
Write-Host "Serving $dir on http://$($ip):$port"
while ($listener.IsListening) {
    try {
        $ctx = $listener.GetContext()
        $path = $ctx.Request.Url.LocalPath.TrimStart('/')
        if ($path -eq '') { $path = 'trade-journal.html' }
        $full = Join-Path $dir $path
        if (Test-Path $full) {
            $bytes = [System.IO.File]::ReadAllBytes($full)
            $ext = [System.IO.Path]::GetExtension($full)
            $mime = @{'.html'='text/html';'.js'='application/javascript';'.css'='text/css';'.png'='image/png';'.ico'='image/x-icon';'.json'='application/json'}
            $ctx.Response.ContentType = $mime.GetValueOrDefault($ext, 'application/octet-stream')
            $ctx.Response.ContentLength64 = $bytes.Length
            $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
        } else {
            $ctx.Response.StatusCode = 404
            $err = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found")
            $ctx.Response.OutputStream.Write($err, 0, $err.Length)
        }
    } catch {
        Write-Host "Error: $_"
    } finally {
        try { $ctx.Response.Close() } catch {}
    }
}
