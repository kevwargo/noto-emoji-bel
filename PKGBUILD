pkgname=noto-emoji-bel
pkgver=1.1
pkgrel=1
pkgdesc="Noto Color Emoji with Belarusian flag"
arch=(any)
license=(OFL-1.1-no-RFN)
depends=(fontconfig noto-fonts-emoji uv)

source=(belarus_s0.png ttf-replace-glyph.py pacman.hook)
sha256sums=(SKIP SKIP SKIP)

package() {
    install -Dm755 ttf-replace-glyph.py $pkgdir/usr/bin/ttf-replace-glyph
    install -Dm644 belarus_s0.png $pkgdir/usr/share/fonts/noto-emoji-bel/belarus_s0.png
    install -Dm644 pacman.hook $pkgdir/usr/share/libalpm/hooks/noto-emoji-bel.hook
}
