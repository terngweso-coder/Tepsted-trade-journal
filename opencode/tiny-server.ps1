$port = 8080
$root = "C:\Users\katak\AppData\Local\Temp\opencode"
$ip = "192.168.100.57"
$endpoint = [System.Net.IPEndPoint]::new([System.Net.IPAddress]::Parse($ip), $port)
$tcp = [System.Net.Sockets.TcpListener]::new($endpoint)
$tcp.Start()
Write-Host "Serving $root on http://$($ip):$port"

while ($true) {
    $client = $tcp.AcceptTcpClient()
    $stream = $client.GetStream()
    $reader = [System.IO.StreamReader]::new($stream)
    $line = $reader.ReadLine()
    if ($line -match 'GET /(\S*)') {
        $path = $Matches[1]
        if ($path -eq '' -or $path -eq '/') { $path = 'trade-journal.html' }
        $full = Join-Path $root $path
        if (Test-Path $full) {
            [byte[]]$body = [System.IO.File]::ReadAllBytes($full)
        } else {
            $body = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found")
        }
        $header = "HTTP/1.1 200 OK`r`nContent-Length: $($body.Length)`r`nContent-Type: text/html; charset=utf-8`r`nAccess-Control-Allow-Origin: *`r`n`r`n"
        $writer = [System.IO.StreamWriter]::new($stream)
        $writer.Write($header)
        $writer.Flush()
        $stream.Write($body, 0, $body.Length)
    }
    $stream.Close()
    $client.Close()
}
