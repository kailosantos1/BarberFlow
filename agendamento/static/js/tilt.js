// Aplica efeito 3D de inclinação + brilho seguindo o mouse em qualquer elemento com a classe .tilt
document.querySelectorAll('.tilt').forEach(function(card) {
    const intensidade = 10; // graus máximos de inclinação

    card.addEventListener('mousemove', function(e) {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const rotX = ((y / rect.height) - 0.5) * -intensidade;
        const rotY = ((x / rect.width) - 0.5) * intensidade;

        card.style.transform = `perspective(800px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(1.02)`;
        card.style.setProperty('--brilho-x', `${x}px`);
        card.style.setProperty('--brilho-y', `${y}px`);
    });

    card.addEventListener('mouseleave', function() {
        card.style.transform = 'perspective(800px) rotateX(0) rotateY(0) scale(1)';
    });
});