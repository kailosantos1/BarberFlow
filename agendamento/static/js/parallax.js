// Efeito parallax: a imagem do hero se move mais devagar que o scroll da página,
// criando sensação de profundidade tanto ao descer quanto ao subir.
const heroBg = document.getElementById('heroBg');

if (heroBg) {
    let ticking = false;

    function moverParallax() {
        const scrollY = window.scrollY;
        const velocidade = 0.4; // quanto menor, mais "lenta" a imagem se move (mais profundidade)
        heroBg.style.transform = `translateY(${scrollY * velocidade}px)`;
        ticking = false;
    }

    window.addEventListener('scroll', function() {
        if (!ticking) {
            window.requestAnimationFrame(moverParallax);
            ticking = true;
        }
    });
}