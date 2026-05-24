$port = 8080
$dir = "C:\Users\katak\AppData\Local\Temp\opencode"
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://+:$port/")
$listener.Start()
Write-Host "Server running on http://0.0.0.0:$port"
while ($listener.IsListening) {
    $ctx = $listener.GetContext()
    $path = $ctx.Request.Url.LocalPath.TrimStart('/')
    if ($path -eq '') { $path = 'trade-journal.html' }
    $full = Join-Path $dir $path
    if (Test-Path $full) {
        $bytes = [System.IO.File]::ReadAllBytes($full)
        $ext = [System.IO.Path]::GetExtension($full)
        $mime = @{'.html'='text/html';'.js'='application/javascript';'.css'='text/css';'.png'='image/png';'.ico'='image/x-icon';'.json'='application/json'}
        $ctx.Response.ContentType = if ($mime.ContainsKey($ext)) { $mime[$ext] } else { 'application/octet-stream' }
        $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
    } else {
        $ctx.Response.StatusCode = 404
        $err = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found")
        $ctx.Response.OutputStream.Write($err, 0, $err.Length)
    }
    $ctx.Response.Close()
}
