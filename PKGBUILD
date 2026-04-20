pkgname=noto-emoji-font-bel
pkgver=1.0
pkgrel=1
pkgdesc="Noto Color Emoji with Belarusian flag"
arch=(any)
license=(OFL-1.1-no-RFN)
depends=(fontconfig)
source=(NotoColorEmoji-bel.ttf 75-noto-emoji-bel.conf)

sha256sums=(SKIP SKIP)

package() {
  install -Dm644 NotoColorEmoji-bel.ttf "$pkgdir/usr/share/fonts/noto-bel/NotoColorEmoji-bel.ttf"
  install -Dm644 75-noto-emoji-bel.conf "$pkgdir/usr/share/fontconfig/conf.avail/75-noto-emoji-bel.conf"
  mkdir -p "$pkgdir/usr/share/fontconfig/conf.default"
  ln -s ../conf.avail/75-noto-emoji-bel.conf "$pkgdir/usr/share/fontconfig/conf.default/75-noto-emoji-bel.conf"
}
