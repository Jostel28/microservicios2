# Descripción: Script para probar los servicios de usuarios y pedidos

function Test-Endpoint {
    param (
        [string]$Url
    )
    try {
        $response = Invoke-WebRequest -Uri $Url -Method GET -ErrorAction Stop
        Write-Output "✔ Endpoint $Url está disponible. Código de respuesta: $($response.StatusCode)"
        return $true
    }
    catch {
        Write-Output "✖ Error al conectar con el endpoint $Url. Detalles: $($_.Exception.Message)"
        return $false
    }
}

function Test-Service-Usuarios {
    Write-Output "Probando servicio de usuarios..."

    # Verificar estado del servicio de usuarios
    $healthUrl = "http://localhost:5000/health"
    if (-not (Test-Endpoint -Url $healthUrl)) { return }

    # Probar obtener todos los usuarios
    $usuariosUrl = "http://localhost:5000/api/usuarios"
    Test-Endpoint -Url $usuariosUrl

    # Probar obtener un usuario específico
    $usuarioEspecificoUrl = "http://localhost:5000/api/usuarios/1"
    Test-Endpoint -Url $usuarioEspecificoUrl
}

function Test-Service-Pedidos {
    Write-Output "Probando servicio de pedidos..."

    # Verificar estado del servicio de pedidos
    $healthUrl = "http://localhost:5001/health"
    if (-not (Test-Endpoint -Url $healthUrl)) { return }

    # Probar obtener todos los pedidos
    $pedidosUrl = "http://localhost:5001/api/pedidos"
    Test-Endpoint -Url $pedidosUrl

    # Probar obtener pedidos para un usuario específico
    $pedidosUsuarioUrl = "http://localhost:5001/api/pedidos/usuario/1"
    Test-Endpoint -Url $pedidosUsuarioUrl
}

# Ejecutar pruebas
Write-Output "Iniciando pruebas de los microservicios..."
Test-Service-Usuarios
Test-Service-Pedidos
Write-Output "Pruebas completadas."