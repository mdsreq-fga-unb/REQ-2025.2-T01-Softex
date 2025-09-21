let users = [
    { id: 1, name: 'João Silva', email: 'joao@softex.com', department: 'Desenvolvimento', role: 'Administrador', status: 'Ativo' },
    { id: 2, name: 'Maria Santos', email: 'maria@softex.com', department: 'Marketing', role: 'Gerente', status: 'Ativo' },
    { id: 3, name: 'Pedro Lima', email: 'pedro@softex.com', department: 'Vendas', role: 'Usuário', status: 'Ativo' },
    { id: 4, name: 'Ana Costa', email: 'ana@softex.com', department: 'RH', role: 'Usuário', status: 'Inativo' }
];

let reservations = [
    { id: 1, user: 'Maria Santos', space: 'Sala Zeus', date: '2024-01-15', time: '14:30-16:00', status: 'Confirmada' },
    { id: 2, user: 'Pedro Lima', space: 'Posição A-15', date: '2024-01-15', time: '08:00-17:00', status: 'Em uso' },
    { id: 3, user: 'Ana Costa', space: 'Sala Hermes', date: '2024-01-15', time: '15:00-16:30', status: 'Agendada' },
    { id: 4, user: 'Carlos Oliveira', space: 'Posição B-08', date: '2024-01-15', time: '13:00-17:00', status: 'Confirmada' }
];

let nextUserId = 5;
let nextReservationId = 5;
let currentUser = null;

const meetingRooms = [
    { name: 'Sala Zeus', capacity: 12, status: 'occupied' },
    { name: 'Sala Hermes', capacity: 8, status: 'reserved' },
    { name: 'Sala Apolo', capacity: 6, status: 'available' },
    { name: 'Sala Atena', capacity: 10, status: 'available' },
    { name: 'Sala Poseidon', capacity: 15, status: 'occupied' },
    { name: 'Sala Ártemis', capacity: 4, status: 'available' }
];

// Authentication functions
function loginWithGoogle() {
    // Simulate Google SSO login
    showNotification('Redirecionando para Google SSO...', 'info');
    setTimeout(() => {
        currentUser = { name: 'João Silva', email: 'joao@softex.com', role: 'Administrador' };
        loginUser();
    }, 2000);
}

function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = input.nextElementSibling.querySelector('i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

function demoLogin(type) {
    if (type === 'admin') {
        currentUser = { name: 'João Silva', email: 'joao@softex.com', role: 'Administrador' };
    } else {
        currentUser = { name: 'Maria Santos', email: 'maria@softex.com', role: 'Usuário' };
    }
    
    loginUser();
}

function loginUser() {
    // Update user info in header
    document.getElementById('currentUser').textContent = currentUser.name;
    document.getElementById('userRole').textContent = currentUser.role;
    document.getElementById('userAvatar').textContent = currentUser.name.split(' ').map(n => n[0]).join('');
    
    // Hide auth screen and show main app
    document.getElementById('authScreen').classList.add('hidden');
    document.getElementById('mainApp').classList.remove('hidden');
    
    // Setup navigation based on user role
    setupNavigation();
    
    // Initialize the app
    initializeApp();
    
    showNotification(`Bem-vindo, ${currentUser.name}!`, 'success');
}

function setupNavigation() {
    const navigationMenu = document.getElementById('navigationMenu');
    navigationMenu.innerHTML = '';
    
    if (currentUser.role === 'Administrador') {
        // Admin navigation
        navigationMenu.innerHTML = `
            <button onclick="showSection('dashboard')" class="nav-btn py-4 px-2 border-b-2 border-[#4A2BE1] text-[#4A2BE1] font-medium">
                <i class="fas fa-tachometer-alt mr-2"></i>Dashboard
            </button>
            <button onclick="showSection('coworking')" class="nav-btn py-4 px-2 border-b-2 border-transparent text-gray-500 hover:text-gray-700">
                <i class="fas fa-map mr-2"></i>Coworking
            </button>
            <button onclick="showSection('reservations')" class="nav-btn py-4 px-2 border-b-2 border-transparent text-gray-500 hover:text-gray-700">
                <i class="fas fa-calendar-alt mr-2"></i>Reservas
            </button>
            <button onclick="showSection('reports')" class="nav-btn py-4 px-2 border-b-2 border-transparent text-gray-500 hover:text-gray-700">
                <i class="fas fa-chart-bar mr-2"></i>Relatórios
            </button>
            <button onclick="showSection('users')" class="nav-btn py-4 px-2 border-b-2 border-transparent text-gray-500 hover:text-gray-700">
                <i class="fas fa-users mr-2"></i>Usuários
            </button>
            <button onclick="showSection('integrations')" class="nav-btn py-4 px-2 border-b-2 border-transparent text-gray-500 hover:text-gray-700">
                <i class="fas fa-plug mr-2"></i>Integrações
            </button>
        `;
    } else {
        // User navigation
        navigationMenu.innerHTML = `
            <button onclick="showSection('coworking')" class="nav-btn py-4 px-2 border-b-2 border-[#4A2BE1] text-[#4A2BE1] font-medium">
                <i class="fas fa-map mr-2"></i>Coworking
            </button>
            <button onclick="showSection('meetingRooms')" class="nav-btn py-4 px-2 border-b-2 border-transparent text-gray-500 hover:text-gray-700">
                <i class="fas fa-door-open mr-2"></i>Salas de Reunião
            </button>
        `;
    }
}

function logout() {
    if (confirm('Tem certeza que deseja sair?')) {
        currentUser = null;
        document.getElementById('authScreen').classList.remove('hidden');
        document.getElementById('mainApp').classList.add('hidden');
        
        // Reset forms
        document.getElementById('loginFormElement').reset();
        document.getElementById('registerFormElement').reset();
        
        showNotification('Logout realizado com sucesso!', 'info');
    }
}

// Form handlers for authentication
document.getElementById('loginFormElement').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    // Simple validation (in real app, this would be server-side)
    if (email && password) {
        // Find user by email (demo purposes)
        const user = users.find(u => u.email === email);
        if (user) {
            currentUser = { name: user.name, email: user.email, role: user.role };
            loginUser();
        } else {
            showNotification('Email ou senha incorretos!', 'error');
        }
    }
});

document.getElementById('registerFormElement').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const firstName = document.getElementById('registerFirstName').value;
    const lastName = document.getElementById('registerLastName').value;
    const email = document.getElementById('registerEmail').value;
    const department = document.getElementById('registerDepartment').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('registerConfirmPassword').value;
    
    // Validation
    if (password !== confirmPassword) {
        showNotification('As senhas não coincidem!', 'error');
        return;
    }
    
    if (password.length < 8) {
        showNotification('A senha deve ter pelo menos 8 caracteres!', 'error');
        return;
    }
    
    // Check if email already exists
    if (users.find(u => u.email === email)) {
        showNotification('Este email já está cadastrado!', 'error');
        return;
    }
    
    // Create new user
    const newUser = {
        id: nextUserId++,
        name: `${firstName} ${lastName}`,
        email: email,
        department: department,
        role: 'Usuário',
        status: 'Ativo'
    };
    
    users.push(newUser);
    currentUser = { name: newUser.name, email: newUser.email, role: newUser.role };
    
    showNotification('Conta criada com sucesso!', 'success');
    setTimeout(() => {
        loginUser();
    }, 1500);
});

// Navigation
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.add('hidden');
    });
    
    // Show selected section
    document.getElementById(sectionName).classList.remove('hidden');
    
    // Update navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('border-[#4A2BE1]', 'text-[#4A2BE1]');
        btn.classList.add('border-transparent', 'text-gray-500');
    });
    
    event.target.classList.remove('border-transparent', 'text-gray-500');
    event.target.classList.add('border-[#4A2BE1]', 'text-[#4A2BE1]');
}

// Interactive seat selection
function selectSeat(seatId) {
    // Remove previous selection
    document.querySelectorAll('.seat-point.selected').forEach(seat => {
        seat.classList.remove('selected');
    });
    
    // Select current seat
    const seatElement = document.querySelector(`[data-seat="${seatId}"]`);
    seatElement.classList.add('selected');
    
    // Show reservation modal
    showReservationModal(seatId);
}

function showReservationModal(seatId) {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="bg-white rounded-xl shadow-xl p-6 w-full max-w-md mx-4">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-semibold text-gray-900">Reservar Posição ${seatId}</h3>
                <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-gray-600">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <form onsubmit="makeReservation(event, '${seatId}')" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Data</label>
                    <input type="date" id="reservationDate" required 
                           class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4A2BE1] focus:border-[#4A2BE1]">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Período</label>
                    <select id="reservationPeriod" required 
                            class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4A2BE1] focus:border-[#4A2BE1]">
                        <option value="">Selecione o período</option>
                        <option value="morning">Manhã (08:00 - 12:00)</option>
                        <option value="afternoon">Tarde (13:00 - 17:00)</option>
                        <option value="fullday">Dia Inteiro (08:00 - 17:00)</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Observações (opcional)</label>
                    <textarea id="reservationNotes" rows="3" 
                              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4A2BE1] focus:border-[#4A2BE1]"
                              placeholder="Alguma observação especial..."></textarea>
                </div>
                <div class="flex space-x-3 pt-4">
                    <button type="button" onclick="this.closest('.fixed').remove()" 
                            class="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-400 transition-colors">
                        Cancelar
                    </button>
                    <button type="submit" 
                            class="flex-1 bg-[#4A2BE1] text-white py-2 px-4 rounded-lg hover:bg-[#4A2BE1] hover:opacity-90 transition-all">
                        Confirmar Reserva
                    </button>
                </div>
            </form>
        </div>
    `;
    document.body.appendChild(modal);
    
    // Set today as default date
    document.getElementById('reservationDate').valueAsDate = new Date();
}

function makeReservation(event, seatId) {
    event.preventDefault();
    
    const date = document.getElementById('reservationDate').value;
    const period = document.getElementById('reservationPeriod').value;
    const notes = document.getElementById('reservationNotes').value;
    
    // Update seat status
    const seatElement = document.querySelector(`[data-seat="${seatId}"]`);
    seatElement.classList.remove('available', 'selected');
    seatElement.classList.add('user-reserved');
    seatElement.removeAttribute('onclick');
    
    // Add to reservations
    const newReservation = {
        id: nextReservationId++,
        user: currentUser.name,
        space: `Posição ${seatId}`,
        date: date,
        time: period === 'morning' ? '08:00-12:00' : period === 'afternoon' ? '13:00-17:00' : '08:00-17:00',
        status: 'Confirmada',
        notes: notes
    };
    
    reservations.push(newReservation);
    
    // Close modal
    document.querySelector('.fixed').remove();
    
    showNotification(`Posição ${seatId} reservada com sucesso!`, 'success');
}

// Initialize coworking grid
function initializeCoworkingGrid() {
    const grid = document.getElementById('coworkingGrid');
    const statuses = ['available', 'occupied', 'reserved'];
    
    for (let i = 1; i <= 58; i++) {
        const seat = document.createElement('div');
        const status = statuses[Math.floor(Math.random() * statuses.length)];
        seat.className = `seat ${status} w-8 h-8 rounded cursor-pointer flex items-center justify-center text-white text-xs font-bold`;
        seat.textContent = i;
        seat.title = `Posição ${String.fromCharCode(65 + Math.floor((i-1)/10))}-${String(i).padStart(2, '0')} - ${status === 'available' ? 'Disponível' : status === 'occupied' ? 'Ocupado' : 'Reservado'}`;
        
        seat.addEventListener('click', () => {
            alert(`Posição ${seat.title.split(' - ')[0]} selecionada`);
        });
        
        grid.appendChild(seat);
    }
}

// Initialize meeting rooms grid
function initializeMeetingRoomsGrid() {
    const container = document.getElementById('meetingRoomsGrid');
    
    meetingRooms.forEach(room => {
        const roomCard = document.createElement('div');
        roomCard.className = `bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow cursor-pointer`;
        roomCard.innerHTML = `
            <div class="p-6">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold text-gray-900">${room.name}</h3>
                    <span class="text-xs px-3 py-1 rounded-full ${
                        room.status === 'available' ? 'bg-green-100 text-green-800' :
                        room.status === 'occupied' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                    }">
                        ${room.status === 'available' ? 'Disponível' : room.status === 'occupied' ? 'Ocupado' : 'Reservado'}
                    </span>
                </div>
                
                <div class="mb-4">
                    <div class="flex items-center text-sm text-gray-600 mb-2">
                        <i class="fas fa-users mr-2 text-[#4A2BE1]"></i>
                        Capacidade: ${room.capacity} pessoas
                    </div>
                    <div class="flex items-center text-sm text-gray-600 mb-2">
                        <i class="fas fa-tv mr-2 text-[#4A2BE1]"></i>
                        TV/Projetor incluído
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                        <i class="fas fa-wifi mr-2 text-[#4A2BE1]"></i>
                        Wi-Fi de alta velocidade
                    </div>
                </div>
                
                <!-- Room floor plan preview -->
                <div class="bg-gray-50 p-3 rounded-lg mb-4">
                    <div class="text-xs text-gray-600 mb-2">Planta Baixa:</div>
                    ${getRoomFloorPlan(room.name)}
                </div>
                
                <button onclick="showRoomDetails('${room.name}')" 
                        class="w-full bg-[#4A2BE1] text-white py-2 px-4 rounded-lg hover:bg-[#4A2BE1] hover:opacity-90 transition-all ${room.status !== 'available' ? 'opacity-50 cursor-not-allowed' : ''}">
                    ${room.status === 'available' ? 'Ver Detalhes & Reservar' : 'Ver Detalhes'}
                </button>
            </div>
        `;
        
        container.appendChild(roomCard);
    });
}

function getRoomFloorPlan(roomName) {
    const plans = {
        'Sala Zeus': `
            <svg viewBox="0 0 120 80" class="w-full h-16">
                <rect x="5" y="5" width="110" height="70" fill="none" stroke="#9CA3AF" stroke-width="1"/>
                <rect x="20" y="25" width="80" height="30" fill="#F59E0B" rx="4"/>
                <circle cx="30" cy="20" r="3" fill="#4A2BE1"/>
                <circle cx="50" cy="20" r="3" fill="#4A2BE1"/>
                <circle cx="70" cy="20" r="3" fill="#4A2BE1"/>
                <circle cx="90" cy="20" r="3" fill="#4A2BE1"/>
                <circle cx="30" cy="60" r="3" fill="#4A2BE1"/>
                <circle cx="50" cy="60" r="3" fill="#4A2BE1"/>
                <circle cx="70" cy="60" r="3" fill="#4A2BE1"/>
                <circle cx="90" cy="60" r="3" fill="#4A2BE1"/>
                <circle cx="15" cy="40" r="3" fill="#4A2BE1"/>
                <circle cx="105" cy="40" r="3" fill="#4A2BE1"/>
                <rect x="105" y="15" width="10" height="6" fill="#1F2937"/>
            </svg>
        `,
        'Sala Hermes': `
            <svg viewBox="0 0 120 80" class="w-full h-16">
                <rect x="5" y="5" width="110" height="70" fill="none" stroke="#9CA3AF" stroke-width="1"/>
                <ellipse cx="60" cy="40" rx="32" ry="16" fill="#80E4F9"/>
                <circle cx="40" cy="32" r="3" fill="#4A2BE1"/>
                <circle cx="48" cy="26" r="3" fill="#4A2BE1"/>
                <circle cx="72" cy="26" r="3" fill="#4A2BE1"/>
                <circle cx="80" cy="32" r="3" fill="#4A2BE1"/>
                <circle cx="80" cy="48" r="3" fill="#4A2BE1"/>
                <circle cx="72" cy="54" r="3" fill="#4A2BE1"/>
                <circle cx="48" cy="54" r="3" fill="#4A2BE1"/>
                <circle cx="40" cy="48" r="3" fill="#4A2BE1"/>
                <rect x="10" y="20" width="20" height="12" fill="white" stroke="#9CA3AF"/>
            </svg>
        `,
        'Sala Apolo': `
            <svg viewBox="0 0 120 80" class="w-full h-16">
                <rect x="5" y="5" width="110" height="70" fill="none" stroke="#9CA3AF" stroke-width="1"/>
                <rect x="32" y="28" width="56" height="24" fill="#F142FB" rx="3"/>
                <circle cx="40" cy="24" r="3" fill="#4A2BE1"/>
                <circle cx="60" cy="24" r="3" fill="#4A2BE1"/>
                <circle cx="80" cy="24" r="3" fill="#4A2BE1"/>
                <circle cx="40" cy="56" r="3" fill="#4A2BE1"/>
                <circle cx="60" cy="56" r="3" fill="#4A2BE1"/>
                <circle cx="80" cy="56" r="3" fill="#4A2BE1"/>
                <rect x="10" y="10" width="16" height="8" fill="#6B7280"/>
                <rect x="92" y="36" width="6" height="8" fill="#1F2937"/>
            </svg>
        `,
        'Sala Atena': `
            <svg viewBox="0 0 120 80" class="w-full h-16">
                <rect x="5" y="5" width="110" height="70" fill="none" stroke="#9CA3AF" stroke-width="1"/>
                <rect x="24" y="20" width="72" height="12" fill="#0A1A3D" rx="2"/>
                <rect x="24" y="48" width="72" height="12" fill="#0A1A3D" rx="2"/>
                <rect x="24" y="32" width="12" height="16" fill="#0A1A3D" rx="2"/>
                <rect x="84" y="32" width="12" height="16" fill="#0A1A3D" rx="2"/>
                <circle cx="32" cy="16" r="3" fill="#4A2BE1"/>
                <circle cx="48" cy="16" r="3" fill="#4A2BE1"/>
                <circle cx="72" cy="16" r="3" fill="#4A2BE1"/>
                <circle cx="88" cy="16" r="3" fill="#4A2BE1"/>
                <circle cx="32" cy="64" r="3" fill="#4A2BE1"/>
                <circle cx="48" cy="64" r="3" fill="#4A2BE1"/>
                <circle cx="72" cy="64" r="3" fill="#4A2BE1"/>
                <circle cx="88" cy="64" r="3" fill="#4A2BE1"/>
                <circle cx="20" cy="40" r="3" fill="#4A2BE1"/>
                <circle cx="100" cy="40" r="3" fill="#4A2BE1"/>
            </svg>
        `,
        'Sala Poseidon': `
            <svg viewBox="0 0 120 80" class="w-full h-16">
                <rect x="5" y="5" width="110" height="70" fill="none" stroke="#9CA3AF" stroke-width="1"/>
                <rect x="16" y="24" width="88" height="32" fill="#F59E0B" rx="4"/>
                <circle cx="24" cy="20" r="3" fill="#4A2BE1"/>
                <circle cx="36" cy="20" r="3" fill="#4A2BE1"/>
                <circle cx="48" cy="20" r="3" fill="#4A2BE1"/>
                <circle cx="60" cy="20" r="3" fill="#4A2BE1"/>
                <circle cx="72" cy="20" r="3" fill="#4A2BE1"/>
                <circle cx="84" cy="20" r="3" fill="#4A2BE1"/>
                <circle cx="96" cy="20" r="3" fill="#4A2BE1"/>
                <circle cx="24" cy="60" r="3" fill="#4A2BE1"/>
                <circle cx="36" cy="60" r="3" fill="#4A2BE1"/>
                <circle cx="48" cy="60" r="3" fill="#4A2BE1"/>
                <circle cx="60" cy="60" r="3" fill="#4A2BE1"/>
                <circle cx="72" cy="60" r="3" fill="#4A2BE1"/>
                <circle cx="84" cy="60" r="3" fill="#4A2BE1"/>
                <circle cx="96" cy="60" r="3" fill="#4A2BE1"/>
                <circle cx="12" cy="40" r="3" fill="#F142FB"/>
                <rect x="108" y="12" width="6" height="10" fill="#1F2937"/>
                <rect x="108" y="58" width="6" height="10" fill="#1F2937"/>
            </svg>
        `,
        'Sala Ártemis': `
            <svg viewBox="0 0 120 80" class="w-full h-16">
                <rect x="5" y="5" width="110" height="70" fill="none" stroke="#9CA3AF" stroke-width="1"/>
                <circle cx="60" cy="40" r="16" fill="#80E4F9"/>
                <circle cx="60" cy="24" r="3" fill="#4A2BE1"/>
                <circle cx="76" cy="40" r="3" fill="#4A2BE1"/>
                <circle cx="60" cy="56" r="3" fill="#4A2BE1"/>
                <circle cx="44" cy="40" r="3" fill="#4A2BE1"/>
                <rect x="88" y="16" width="24" height="10" fill="#6B7280" rx="5"/>
                <rect x="92" y="32" width="16" height="8" fill="#F59E0B" rx="2"/>
                <circle cx="20" cy="20" r="6" fill="#10B981"/>
            </svg>
        `
    };
    
    return plans[roomName] || '<div class="text-center text-gray-400">Planta não disponível</div>';
}

function showRoomDetails(roomName) {
    const room = meetingRooms.find(r => r.name === roomName);
    if (!room) return;
    
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4';
    modal.innerHTML = `
        <div class="bg-white rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold text-gray-900">${room.name}</h2>
                    <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-gray-600">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div>
                        <h3 class="text-lg font-semibold text-gray-900 mb-3">Especificações</h3>
                        <div class="space-y-2">
                            <div class="flex items-center text-sm text-gray-600">
                                <i class="fas fa-users mr-3 text-[#4A2BE1] w-4"></i>
                                Capacidade: ${room.capacity} pessoas
                            </div>
                            <div class="flex items-center text-sm text-gray-600">
                                <i class="fas fa-tv mr-3 text-[#4A2BE1] w-4"></i>
                                TV 55" com HDMI/USB
                            </div>
                            <div class="flex items-center text-sm text-gray-600">
                                <i class="fas fa-wifi mr-3 text-[#4A2BE1] w-4"></i>
                                Wi-Fi de alta velocidade
                            </div>
                            <div class="flex items-center text-sm text-gray-600">
                                <i class="fas fa-marker mr-3 text-[#4A2BE1] w-4"></i>
                                Quadro branco
                            </div>
                            <div class="flex items-center text-sm text-gray-600">
                                <i class="fas fa-snowflake mr-3 text-[#4A2BE1] w-4"></i>
                                Ar condicionado
                            </div>
                            <div class="flex items-center text-sm text-gray-600">
                                <i class="fas fa-coffee mr-3 text-[#4A2BE1] w-4"></i>
                                Serviço de café (opcional)
                            </div>
                        </div>
                    </div>
                    
                    <div>
                        <h3 class="text-lg font-semibold text-gray-900 mb-3">Planta Baixa</h3>
                        <div class="bg-gray-50 p-4 rounded-lg">
                            ${getRoomFloorPlan(room.name)}
                        </div>
                    </div>
                </div>
                
                ${room.status === 'available' ? `
                    <div class="border-t pt-6">
                        <h3 class="text-lg font-semibold text-gray-900 mb-4">Fazer Reserva</h3>
                        <form onsubmit="makeRoomReservation(event, '${room.name}')" class="space-y-4">
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Data</label>
                                    <input type="date" id="roomReservationDate" required 
                                           class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4A2BE1] focus:border-[#4A2BE1]">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Horário</label>
                                    <select id="roomReservationTime" required 
                                            class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4A2BE1] focus:border-[#4A2BE1]">
                                        <option value="">Selecione o horário</option>
                                        <option value="08:00-09:00">08:00 - 09:00</option>
                                        <option value="09:00-10:00">09:00 - 10:00</option>
                                        <option value="10:00-11:00">10:00 - 11:00</option>
                                        <option value="11:00-12:00">11:00 - 12:00</option>
                                        <option value="14:00-15:00">14:00 - 15:00</option>
                                        <option value="15:00-16:00">15:00 - 16:00</option>
                                        <option value="16:00-17:00">16:00 - 17:00</option>
                                        <option value="17:00-18:00">17:00 - 18:00</option>
                                    </select>
                                </div>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Finalidade da reunião</label>
                                <input type="text" id="roomReservationPurpose" required 
                                       class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4A2BE1] focus:border-[#4A2BE1]"
                                       placeholder="Ex: Reunião de projeto, apresentação para cliente...">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Número de participantes</label>
                                <input type="number" id="roomReservationParticipants" min="1" max="${room.capacity}" required 
                                       class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#4A2BE1] focus:border-[#4A2BE1]"
                                       placeholder="Quantas pessoas participarão?">
                            </div>
                            <div class="flex space-x-3 pt-4">
                                <button type="button" onclick="this.closest('.fixed').remove()" 
                                        class="flex-1 bg-gray-300 text-gray-700 py-3 px-4 rounded-lg hover:bg-gray-400 transition-colors">
                                    Cancelar
                                </button>
                                <button type="submit" 
                                        class="flex-1 bg-[#4A2BE1] text-white py-3 px-4 rounded-lg hover:bg-[#4A2BE1] hover:opacity-90 transition-all">
                                    Confirmar Reserva
                                </button>
                            </div>
                        </form>
                    </div>
                ` : `
                    <div class="border-t pt-6 text-center">
                        <div class="text-gray-500">
                            <i class="fas fa-lock text-2xl mb-2"></i>
                            <p>Esta sala está ${room.status === 'occupied' ? 'ocupada' : 'reservada'} no momento.</p>
                        </div>
                    </div>
                `}
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    
    // Set today as default date
    if (room.status === 'available') {
        document.getElementById('roomReservationDate').valueAsDate = new Date();
    }
}

function makeRoomReservation(event, roomName) {
    event.preventDefault();
    
    const date = document.getElementById('roomReservationDate').value;
    const time = document.getElementById('roomReservationTime').value;
    const purpose = document.getElementById('roomReservationPurpose').value;
    const participants = document.getElementById('roomReservationParticipants').value;
    
    // Add to reservations
    const newReservation = {
        id: nextReservationId++,
        user: currentUser.name,
        space: roomName,
        date: date,
        time: time,
        status: 'Confirmada',
        purpose: purpose,
        participants: participants
    };
    
    reservations.push(newReservation);
    
    // Update room status
    const room = meetingRooms.find(r => r.name === roomName);
    if (room) {
        room.status = 'reserved';
    }
    
    // Close modal
    document.querySelector('.fixed').remove();
    
    // Refresh meeting rooms grid
    document.getElementById('meetingRoomsGrid').innerHTML = '';
    initializeMeetingRoomsGrid();
    
    showNotification(`${roomName} reservada com sucesso!`, 'success');
}

// Populate users table
function populateUsersTable() {
    const tbody = document.getElementById('usersTable');
    tbody.innerHTML = '';
    
    users.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                    <div class="w-8 h-8 bg-[#4A2BE1] rounded-full flex items-center justify-center text-white text-sm font-bold mr-3">
                        ${user.name.split(' ').map(n => n[0]).join('')}
                    </div>
                    <span class="text-sm font-medium text-gray-900">${user.name}</span>
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${user.email}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${user.department}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${user.role}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs rounded-full ${user.status === 'Ativo' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                    ${user.status}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button onclick="editUser(${user.id})" class="text-blue-600 hover:text-blue-900 mr-3">Editar</button>
                <button onclick="deleteUser(${user.id})" class="text-red-600 hover:text-red-900">Excluir</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Populate reservations table
function populateReservationsTable() {
    const tbody = document.getElementById('reservationsTable');
    tbody.innerHTML = '';
    
    reservations.forEach(reservation => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${reservation.user}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${reservation.space}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${reservation.date}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${reservation.time}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs rounded-full ${
                    reservation.status === 'Confirmada' ? 'bg-green-100 text-green-800' :
                    reservation.status === 'Em uso' ? 'bg-blue-100 text-blue-800' :
                    'bg-yellow-100 text-yellow-800'
                }">
                    ${reservation.status}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button onclick="editReservation(${reservation.id})" class="text-blue-600 hover:text-blue-900 mr-3">Editar</button>
                <button onclick="cancelReservation(${reservation.id})" class="text-red-600 hover:text-red-900">Cancelar</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Modal functions
function showAddUserModal() {
    document.getElementById('addUserModal').classList.remove('hidden');
    document.getElementById('addUserModal').classList.add('flex');
}

function hideAddUserModal() {
    document.getElementById('addUserModal').classList.add('hidden');
    document.getElementById('addUserModal').classList.remove('flex');
}

// Funções dos botões
function filterReservations() {
    const filterModal = document.createElement('div');
    filterModal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    filterModal.innerHTML = `
        <div class="bg-white rounded-xl shadow-xl p-6 w-full max-w-md mx-4">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Filtrar Reservas</h3>
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
                    <select id="filterStatus" class="w-full p-3 border border-gray-300 rounded-lg">
                        <option value="">Todos</option>
                        <option value="Confirmada">Confirmada</option>
                        <option value="Em uso">Em uso</option>
                        <option value="Agendada">Agendada</option>
                    </select>
                </div>
                <div class="flex space-x-3 pt-4">
                    <button onclick="this.closest('.fixed').remove()" class="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg">Cancelar</button>
                    <button onclick="applyFilter()" class="flex-1 bg-[#4A2BE1] text-white py-2 px-4 rounded-lg">Aplicar</button>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(filterModal);
}

function applyFilter() {
    const status = document.getElementById('filterStatus').value;
    const filteredReservations = status ? reservations.filter(r => r.status === status) : reservations;
    
    const tbody = document.getElementById('reservationsTable');
    tbody.innerHTML = '';
    
    filteredReservations.forEach(reservation => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${reservation.user}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${reservation.space}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${reservation.date}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${reservation.time}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 py-1 text-xs rounded-full ${
                    reservation.status === 'Confirmada' ? 'bg-green-100 text-green-800' :
                    reservation.status === 'Em uso' ? 'bg-blue-100 text-blue-800' :
                    'bg-yellow-100 text-yellow-800'
                }">
                    ${reservation.status}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button onclick="editReservation(${reservation.id})" class="text-blue-600 hover:text-blue-900 mr-3">Editar</button>
                <button onclick="cancelReservation(${reservation.id})" class="text-red-600 hover:text-red-900">Cancelar</button>
            </td>
        `;
        tbody.appendChild(row);
    });
    
    document.querySelector('.fixed').remove();
    showNotification('Filtro aplicado com sucesso!', 'success');
}

function exportReservations() {
    const csvContent = "data:text/csv;charset=utf-8," 
        + "Usuário,Espaço,Data,Horário,Status\n"
        + reservations.map(r => `${r.user},${r.space},${r.date},${r.time},${r.status}`).join("\n");
    
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "reservas_softex.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showNotification('Relatório exportado com sucesso!', 'success');
}

function generateReport() {
    showNotification('Gerando relatório personalizado...', 'info');
    setTimeout(() => {
        showNotification('Relatório gerado com sucesso! Dados atualizados.', 'success');
    }, 2000);
}

function configureSlack() {
    const configModal = document.createElement('div');
    configModal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    configModal.innerHTML = `
        <div class="bg-white rounded-xl shadow-xl p-6 w-full max-w-md mx-4">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Configurar Slack</h3>
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Webhook URL</label>
                    <input type="url" placeholder="https://hooks.slack.com/..." class="w-full p-3 border border-gray-300 rounded-lg">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Canal</label>
                    <input type="text" placeholder="#coworking" class="w-full p-3 border border-gray-300 rounded-lg">
                </div>
                <div class="flex space-x-3 pt-4">
                    <button onclick="this.closest('.fixed').remove()" class="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg">Cancelar</button>
                    <button onclick="saveSlackConfig()" class="flex-1 bg-[#F142FB] text-white py-2 px-4 rounded-lg">Salvar</button>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(configModal);
}

function saveSlackConfig() {
    document.querySelector('.fixed').remove();
    showNotification('Configurações do Slack salvas com sucesso!', 'success');
}

function configureGoogle() {
    const configModal = document.createElement('div');
    configModal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    configModal.innerHTML = `
        <div class="bg-white rounded-xl shadow-xl p-6 w-full max-w-md mx-4">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Configurar Google Workspace</h3>
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">ID do Calendário</label>
                    <input type="text" placeholder="calendario@softex.com" class="w-full p-3 border border-gray-300 rounded-lg">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Chave API</label>
                    <input type="password" placeholder="••••••••••••••••" class="w-full p-3 border border-gray-300 rounded-lg">
                </div>
                <div class="flex space-x-3 pt-4">
                    <button onclick="this.closest('.fixed').remove()" class="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg">Cancelar</button>
                    <button onclick="saveGoogleConfig()" class="flex-1 bg-[#80E4F9] text-[#0A1A3D] py-2 px-4 rounded-lg font-medium">Salvar</button>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(configModal);
}

function saveGoogleConfig() {
    document.querySelector('.fixed').remove();
    showNotification('Configurações do Google Workspace salvas com sucesso!', 'success');
}

function editUser(userId) {
    const user = users.find(u => u.id === userId);
    if (user) {
        showNotification(`Editando usuário: ${user.name}`, 'info');
    }
}

function deleteUser(userId) {
    if (confirm('Tem certeza que deseja excluir este usuário?')) {
        users = users.filter(u => u.id !== userId);
        populateUsersTable();
        showNotification('Usuário excluído com sucesso!', 'success');
    }
}

function editReservation(reservationId) {
    const reservation = reservations.find(r => r.id === reservationId);
    if (reservation) {
        showNotification(`Editando reserva: ${reservation.space}`, 'info');
    }
}

function cancelReservation(reservationId) {
    if (confirm('Tem certeza que deseja cancelar esta reserva?')) {
        reservations = reservations.filter(r => r.id !== reservationId);
        populateReservationsTable();
        showNotification('Reserva cancelada com sucesso!', 'success');
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    const bgColor = type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500';
    
    notification.className = `fixed top-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50 transform transition-all duration-300`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Form handlers
document.getElementById('reservationForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const type = document.getElementById('reservationType').value;
    const date = document.getElementById('reservationDate').value;
    const time = document.getElementById('reservationTime').value;
    
    const newReservation = {
        id: nextReservationId++,
        user: currentUser ? currentUser.name : 'Usuário Atual',
        space: type === 'coworking' ? `Posição A-${Math.floor(Math.random() * 58) + 1}` : `Sala ${['Zeus', 'Hermes', 'Apolo'][Math.floor(Math.random() * 3)]}`,
        date: date,
        time: time,
        status: 'Confirmada'
    };
    
    reservations.push(newReservation);
    populateReservationsTable();
    showNotification('Nova reserva criada com sucesso!', 'success');
    
    // Reset form
    this.reset();
    document.getElementById('reservationDate').valueAsDate = new Date();
});

document.getElementById('addUserForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const inputs = this.querySelectorAll('input, select');
    
    const newUser = {
        id: nextUserId++,
        name: inputs[0].value,
        email: inputs[1].value,
        department: inputs[2].value,
        role: inputs[3].value,
        status: 'Ativo'
    };
    
    users.push(newUser);
    populateUsersTable();
    hideAddUserModal();
    showNotification('Usuário adicionado com sucesso!', 'success');
    
    // Reset form
    this.reset();
});

// Initialize app
function initializeApp() {
    if (currentUser.role === 'Administrador') {
        populateUsersTable();
        populateReservationsTable();
        
        // Set current date for admin forms
        const reservationDateField = document.getElementById('reservationDate');
        if (reservationDateField) {
            reservationDateField.valueAsDate = new Date();
        }
    }
    
    // Initialize meeting rooms grid for both admin and user
    initializeMeetingRoomsGrid();
    
    // Show appropriate first section
    if (currentUser.role === 'Administrador') {
        showSection('dashboard');
    } else {
        showSection('coworking');
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // App starts with login screen visible
});