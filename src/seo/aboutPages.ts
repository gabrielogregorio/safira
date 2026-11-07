import type { Locale } from '../language/messages.ts';
import { SEO_LOCALES, SEO_PAGES, SITE_URL } from './seoPages.ts';

export const ABOUT_FOLDER = 'about/';

const REPOSITORY_URL = 'https://github.com/gabrielogregorio/safira';

interface Question {
  question: string;
  answer: string;
}

interface AboutCopy {
  title: string;
  description: string;
  heading: string;
  lead: string;
  openIde: string;
  whoTitle: string;
  who: string[];
  exampleTitle: string;
  exampleText: string;
  outputLabel: string;
  example: string;
  output: string[];
  lessonsTitle: string;
  lessonsText: string;
  questionsTitle: string;
  questions: Question[];
  historyTitle: string;
  history: string;
  linksTitle: string;
  wiki: string;
  github: string;
  changelog: string;
  bug: string;
  languagesLabel: string;
}

// The example runs in a test, so the output shown here is what Safira really prints.
export const ABOUT_PAGES: Record<Locale, AboutCopy> = {
  'en-us': {
    title: 'About Safira: learn to code in plain words, free, in the browser',
    description:
      'What Safira is, who it is for, a short program, the 14 lessons, answers to common questions and links to the wiki and the code.',
    heading: 'About Safira',
    lead: 'Safira is a programming language that reads like plain English, made for people who have never programmed. You write commands the way you would say them, and the program runs right in the browser, on a computer or on a phone.',
    openIde: 'Open the IDE',
    whoTitle: 'Who it is for',
    who: [
      'Anyone writing a first line of code, at any age.',
      'Teachers who want a first class on logic without installing anything.',
      'People who do not read English: Safira also speaks Portuguese, Spanish, Chinese and Japanese.',
    ],
    exampleTitle: 'A short program',
    exampleText: 'A variable, a loop and a condition:',
    outputLabel: 'What it shows',
    example:
      'name = "Ana"\nshow "Hello, " + name + "!"\n\nrepeat 3 times {\n    show "⭐"\n}\n\ngrade = 8\nif grade is greater than or equal to 6 then {\n    show "You passed! 🎉"\n} else {\n    show "Try again."\n}',
    output: ['Hello, Ana!', '⭐', '⭐', '⭐', 'You passed! 🎉'],
    lessonsTitle: 'The 14 lessons',
    lessonsText:
      'Open a project and choose Lesson mode in the Help menu. Each lesson shows a program to run and then a challenge, which Safira checks by itself.',
    questionsTitle: 'Questions',
    questions: [
      { question: 'Is it free?', answer: 'Yes. Safira is open source, under the MIT license.' },
      {
        question: 'Do I need to install anything or create an account?',
        answer: 'No. Open the site in a current browser. There are no accounts.',
      },
      {
        question: 'Does it work on a phone?',
        answer: 'Yes. On a phone the IDE splits into Code, Output and Variables panels.',
      },
      {
        question: 'Does my code go to a server?',
        answer:
          'No. Programs run in the browser and projects stay in this browser. Export a project as a .zip to keep a copy or move it to another device.',
      },
      {
        question: 'Can I mix languages in the same program?',
        answer: 'Yes. Every language is active all the time, even on the same line.',
      },
      {
        question: 'Can I make a game?',
        answer: 'Yes. Programs can read the keyboard. Open Dinosaur or Mini RPG in the Examples menu to see how.',
      },
    ],
    historyTitle: 'History',
    history:
      'Safira started in 2019 as a language and IDE in Python, installed on the computer. In 2026 it was rewritten for the web: now the first line of code is one link away, and scripts from the Python version still run the same.',
    linksTitle: 'Learn more',
    wiki: 'Wiki: guide, commands and recipes',
    github: 'Source code on GitHub',
    changelog: 'What changed in each version',
    bug: 'Report a bug',
    languagesLabel: 'Languages',
  },
  'pt-br': {
    title: 'Sobre a Safira: programar em português, grátis, no navegador',
    description:
      'O que é a Safira, para quem ela é, um programa curto, as 14 aulas, respostas para as dúvidas comuns e links para a wiki e o código.',
    heading: 'Sobre a Safira',
    lead: 'A Safira é uma linguagem de programação em português, feita para quem nunca programou. Você escreve os comandos do jeito que falaria, e o programa roda direto no navegador, no computador ou no celular.',
    openIde: 'Abrir a IDE',
    whoTitle: 'Para quem é',
    who: [
      'Quem vai escrever a primeira linha de código, em qualquer idade.',
      'Professores que querem uma primeira aula de lógica sem instalar nada.',
      'Quem não lê inglês: a Safira fala português, e também inglês, espanhol, chinês e japonês.',
    ],
    exampleTitle: 'Um programa curto',
    exampleText: 'Uma variável, uma repetição e uma condição:',
    outputLabel: 'O que ele mostra',
    example:
      'nome = "Ana"\nmostre "Olá, " + nome + "!"\n\nrepita 3 vezes {\n    mostre "⭐"\n}\n\nnota = 8\nse nota for maior ou igual a 6 então {\n    mostre "Você passou! 🎉"\n} senão {\n    mostre "Tente de novo."\n}',
    output: ['Olá, Ana!', '⭐', '⭐', '⭐', 'Você passou! 🎉'],
    lessonsTitle: 'As 14 aulas',
    lessonsText:
      'Abra um projeto e escolha Modo aula no menu Ajuda. Cada aula mostra um programa para rodar e depois um desafio, que a Safira confere sozinha.',
    questionsTitle: 'Dúvidas',
    questions: [
      { question: 'É grátis?', answer: 'Sim. A Safira é de código aberto, com licença MIT.' },
      {
        question: 'Preciso instalar alguma coisa ou criar conta?',
        answer: 'Não. Abra o site num navegador atual. Não existe conta.',
      },
      {
        question: 'Funciona no celular?',
        answer: 'Sim. No celular a IDE se divide nos painéis Código, Saída e Variáveis.',
      },
      {
        question: 'Meu código vai para algum servidor?',
        answer:
          'Não. Os programas rodam no navegador e os projetos ficam neste navegador. Exporte o projeto em .zip para guardar uma cópia ou levar para outro aparelho.',
      },
      {
        question: 'Posso misturar idiomas no mesmo programa?',
        answer: 'Pode. Todos os idiomas valem o tempo todo, até na mesma linha.',
      },
      {
        question: 'Dá para fazer um jogo?',
        answer: 'Dá. Os programas leem o teclado. Abra Dinossauro ou Mini RPG no menu Exemplos para ver como.',
      },
    ],
    historyTitle: 'História',
    history:
      'A Safira nasceu em 2019 como linguagem e IDE em Python, instalada no computador. Em 2026 ela foi reescrita para a web: agora a primeira linha de código está a um link de distância, e os scripts da versão em Python continuam rodando igual.',
    linksTitle: 'Saiba mais',
    wiki: 'Wiki: guia, comandos e receitas',
    github: 'Código no GitHub',
    changelog: 'O que mudou em cada versão',
    bug: 'Reportar um problema',
    languagesLabel: 'Idiomas',
  },
  es: {
    title: 'Sobre Safira: programar en español, gratis, en el navegador',
    description:
      'Qué es Safira, para quién es, un programa corto, las 14 lecciones, respuestas a las dudas comunes y enlaces a la wiki y al código.',
    heading: 'Sobre Safira',
    lead: 'Safira es un lenguaje de programación en español, hecho para quien nunca programó. Escribes los comandos como los dirías, y el programa funciona directo en el navegador, en el ordenador o en el móvil.',
    openIde: 'Abrir el IDE',
    whoTitle: 'Para quién es',
    who: [
      'Quien va a escribir su primera línea de código, a cualquier edad.',
      'Docentes que quieren una primera clase de lógica sin instalar nada.',
      'Quien no lee inglés: Safira habla español, y también portugués, inglés, chino y japonés.',
    ],
    exampleTitle: 'Un programa corto',
    exampleText: 'Una variable, una repetición y una condición:',
    outputLabel: 'Lo que muestra',
    example:
      'nombre = "Ana"\nmuestra "¡Hola, " + nombre + "!"\n\nrepetir 3 veces {\n    muestra "⭐"\n}\n\nnota = 8\nsi nota es mayor o igual a 6 entonces {\n    muestra "¡Aprobaste! 🎉"\n} si no {\n    muestra "Inténtalo de nuevo."\n}',
    output: ['¡Hola, Ana!', '⭐', '⭐', '⭐', '¡Aprobaste! 🎉'],
    lessonsTitle: 'Las 14 lecciones',
    lessonsText:
      'Abre un proyecto y elige Modo clase en el menú Ayuda. Cada lección muestra un programa para ejecutar y después un desafío, que Safira revisa sola.',
    questionsTitle: 'Dudas',
    questions: [
      { question: '¿Es gratis?', answer: 'Sí. Safira es de código abierto, con licencia MIT.' },
      {
        question: '¿Tengo que instalar algo o crear una cuenta?',
        answer: 'No. Abre el sitio en un navegador actual. No hay cuentas.',
      },
      {
        question: '¿Funciona en el móvil?',
        answer: 'Sí. En el móvil el IDE se divide en los paneles Código, Salida y Variables.',
      },
      {
        question: '¿Mi código va a algún servidor?',
        answer:
          'No. Los programas se ejecutan en el navegador y los proyectos quedan en este navegador. Exporta el proyecto en .zip para guardar una copia o llevarlo a otro dispositivo.',
      },
      {
        question: '¿Puedo mezclar idiomas en el mismo programa?',
        answer: 'Sí. Todos los idiomas valen todo el tiempo, incluso en la misma línea.',
      },
      {
        question: '¿Se puede hacer un juego?',
        answer: 'Sí. Los programas leen el teclado. Abre Dinosaurio o Mini RPG en el menú Ejemplos para ver cómo.',
      },
    ],
    historyTitle: 'Historia',
    history:
      'Safira nació en 2019 como lenguaje e IDE en Python, instalado en el ordenador. En 2026 fue reescrita para la web: ahora la primera línea de código está a un enlace, y los scripts de la versión en Python siguen funcionando igual.',
    linksTitle: 'Saber más',
    wiki: 'Wiki: guía, comandos y recetas',
    github: 'Código en GitHub',
    changelog: 'Qué cambió en cada versión',
    bug: 'Reportar un problema',
    languagesLabel: 'Idiomas',
  },
  'zh-cn': {
    title: '关于 Safira：用中文学编程，免费，直接在浏览器中运行',
    description: 'Safira 是什么、适合谁、一个小程序、14 节课程、常见问题解答，以及维基和源代码的链接。',
    heading: '关于 Safira',
    lead: 'Safira 是一门可以用中文书写的编程语言，专为从没写过代码的人设计。你像说话一样写命令，程序直接在浏览器里运行，电脑和手机都可以。',
    openIde: '打开 IDE',
    whoTitle: '适合谁',
    who: [
      '任何年龄、准备写下第一行代码的人。',
      '想在不安装任何软件的情况下上第一堂逻辑课的老师。',
      '不懂英语的人：Safira 会说中文，也会说英语、葡萄牙语、西班牙语和日语。',
    ],
    exampleTitle: '一个小程序',
    exampleText: '一个变量、一次重复和一个条件：',
    outputLabel: '运行结果',
    example:
      '名字 = "小明"\n显示 "你好，" + 名字 + "！"\n\n重复 3 次 {\n    显示 "⭐"\n}\n\n成绩 = 8\n如果 成绩 大于等于 6 那么 {\n    显示 "你及格了！🎉"\n} 否则 {\n    显示 "再试一次。"\n}',
    output: ['你好，小明！', '⭐', '⭐', '⭐', '你及格了！🎉'],
    lessonsTitle: '14 节课程',
    lessonsText:
      '打开一个项目，在「帮助」菜单中选择「课程模式」。每节课先给出一个可以运行的程序，然后是一个挑战，Safira 会自动检查你的答案。',
    questionsTitle: '常见问题',
    questions: [
      { question: '免费吗？', answer: '免费。Safira 是开源软件，采用 MIT 许可证。' },
      { question: '需要安装软件或注册账号吗？', answer: '不需要。用较新的浏览器打开网站即可，没有账号系统。' },
      { question: '手机上能用吗？', answer: '能。在手机上，IDE 会分成代码、输出和变量三个面板。' },
      {
        question: '我的代码会上传到服务器吗？',
        answer: '不会。程序在浏览器中运行，项目保存在当前浏览器里。把项目导出为 .zip，就能保留副本或换到其他设备。',
      },
      { question: '同一个程序里能混用多种语言吗？', answer: '能。所有语言随时都有效，甚至可以写在同一行。' },
      { question: '能做游戏吗？', answer: '能。程序可以读取键盘。在「示例」菜单中打开恐龙或迷你 RPG 看看。' },
    ],
    historyTitle: '历史',
    history:
      'Safira 诞生于 2019 年，最初是用 Python 编写、安装在电脑上的语言和 IDE。2026 年它被重写为网页版：现在打开一个链接就能写下第一行代码，Python 版本的脚本也照样能运行。',
    linksTitle: '了解更多',
    wiki: '维基：指南、命令和示例',
    github: 'GitHub 上的源代码',
    changelog: '各版本的更新内容',
    bug: '报告问题',
    languagesLabel: '语言',
  },
  ja: {
    title: 'Safira について：日本語でプログラミングを学ぶ、無料、ブラウザで',
    description:
      'Safira とは何か、誰のためのものか、短いプログラム、14 のレッスン、よくある質問への答え、ウィキとソースコードへのリンク。',
    heading: 'Safira について',
    lead: 'Safira は日本語で書けるプログラミング言語で、プログラミングをしたことがない人のために作られました。話すように命令を書くと、プログラムがそのままブラウザで動きます。パソコンでもスマホでも使えます。',
    openIde: 'IDE を開く',
    whoTitle: '誰のためのもの',
    who: [
      '年齢を問わず、はじめてコードを書く人。',
      '何もインストールせずに、論理の最初の授業をしたい先生。',
      '英語が読めない人：Safira は日本語のほか、英語、ポルトガル語、スペイン語、中国語も話します。',
    ],
    exampleTitle: '短いプログラム',
    exampleText: '変数、くり返し、条件：',
    outputLabel: '表示される結果',
    example:
      '名前 = "さくら"\n表示 "こんにちは、" + 名前 + "！"\n\n繰り返す 3 回 {\n    表示 "⭐"\n}\n\n点数 = 8\nもし 点数 以上 6 なら {\n    表示 "合格です! 🎉"\n} そうでなければ {\n    表示 "もう一度がんばりましょう。"\n}',
    output: ['こんにちは、さくら！', '⭐', '⭐', '⭐', '合格です! 🎉'],
    lessonsTitle: '14 のレッスン',
    lessonsText:
      'プロジェクトを開いて、「ヘルプ」メニューから「レッスンモード」を選びます。各レッスンでは、まず動かすプログラムがあり、次にチャレンジがあります。答えは Safira が自動でチェックします。',
    questionsTitle: 'よくある質問',
    questions: [
      { question: '無料ですか？', answer: 'はい。Safira はオープンソースで、MIT ライセンスです。' },
      {
        question: 'インストールやアカウント登録は必要ですか？',
        answer: 'いいえ。新しめのブラウザでサイトを開くだけです。アカウントはありません。',
      },
      { question: 'スマホで使えますか？', answer: 'はい。スマホでは IDE がコード、出力、変数のパネルに分かれます。' },
      {
        question: 'コードはサーバーに送られますか？',
        answer:
          'いいえ。プログラムはブラウザで動き、プロジェクトはこのブラウザに保存されます。.zip で書き出せば、コピーを残したり別の端末に移したりできます。',
      },
      {
        question: '同じプログラムで言語を混ぜられますか？',
        answer: 'はい。すべての言語がいつでも有効で、同じ行でも混ぜられます。',
      },
      {
        question: 'ゲームは作れますか？',
        answer: 'はい。プログラムはキーボードを読めます。「サンプル」メニューの恐竜やミニ RPG を開いてみてください。',
      },
    ],
    historyTitle: '歴史',
    history:
      'Safira は 2019 年に、パソコンにインストールする Python 製の言語と IDE として生まれました。2026 年にウェブ向けに書き直され、今ではリンクひとつで最初の一行が書けます。Python 版のスクリプトも同じように動きます。',
    linksTitle: 'もっと知る',
    wiki: 'ウィキ：ガイド、命令、レシピ',
    github: 'GitHub のソースコード',
    changelog: '各バージョンの変更点',
    bug: '問題を報告する',
    languagesLabel: '言語',
  },
};

const aboutUrl = (locale: Locale): string => `${SITE_URL}${SEO_PAGES[locale].folder}${ABOUT_FOLDER}`;

const escapeHtml = (text: string): string =>
  text.replaceAll('&', '&amp;').replaceAll('"', '&quot;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');

// The English page is one folder deep and the others two: links between pages go up to the site root first.
const toRoot = (locale: Locale): string => (SEO_PAGES[locale].folder === '' ? '../' : '../../');

const STYLE = `
      :root {
        color-scheme: light dark;
        --ink: #12395c;
        --muted: #3d5f7d;
        --page: #eef6fd;
        --card: #ffffff;
        --line: #c9def0;
        --accent: #0b6bcb;
        --code: #0f2a44;
        --code-ink: #e8f2fc;
      }

      @media (prefers-color-scheme: dark) {
        :root {
          --ink: #e2eefa;
          --muted: #a9c3dc;
          --page: #0d1b2a;
          --card: #132638;
          --line: #24405a;
          --accent: #6fb6ff;
          --code: #08131f;
          --code-ink: #e8f2fc;
        }
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        background: var(--page);
        color: var(--ink);
        font-family: system-ui, sans-serif;
        line-height: 1.6;
      }

      main {
        max-width: 760px;
        margin: 0 auto;
        padding: 32px 16px 48px;
      }

      header {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        align-items: center;
        justify-content: space-between;
      }

      .brand {
        display: flex;
        gap: 12px;
        align-items: center;
        color: inherit;
        font-weight: 700;
        font-size: 1.2rem;
        text-decoration: none;
      }

      .open {
        display: inline-block;
        padding: 10px 18px;
        border-radius: 999px;
        background: var(--accent);
        color: #ffffff;
        font-weight: 600;
        text-decoration: none;
      }

      @media (prefers-color-scheme: dark) {
        .open {
          color: #08131f;
        }
      }

      h1 {
        margin: 32px 0 8px;
        font-size: 2rem;
        line-height: 1.2;
      }

      h2 {
        margin: 40px 0 12px;
        font-size: 1.3rem;
      }

      .lead {
        color: var(--muted);
        font-size: 1.1rem;
      }

      section h2 {
        margin-top: 20px;
      }

      section {
        padding: 4px 20px 16px;
        margin-top: 24px;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: var(--card);
      }

      pre {
        overflow-x: auto;
        margin: 0;
        padding: 16px;
        border-radius: 12px;
        background: var(--code);
        color: var(--code-ink);
        font-size: 0.95rem;
      }

      .label {
        margin: 16px 0 6px;
        color: var(--muted);
        font-size: 0.9rem;
      }

      ol {
        columns: 2;
        column-gap: 32px;
      }

      @media (max-width: 520px) {
        ol {
          columns: 1;
        }
      }

      dt {
        margin-top: 16px;
        font-weight: 600;
      }

      dd {
        margin: 4px 0 0;
        color: var(--muted);
      }

      a {
        color: var(--accent);
      }

      footer {
        margin-top: 40px;
        color: var(--muted);
        font-size: 0.95rem;
        text-align: center;
      }
`;

const alternateLinks = (): string =>
  [
    ...SEO_LOCALES.map(
      (locale) => `<link rel="alternate" hreflang="${SEO_PAGES[locale].htmlLang}" href="${aboutUrl(locale)}" />`,
    ),
    `<link rel="alternate" hreflang="x-default" href="${aboutUrl('en-us')}" />`,
  ].join('\n    ');

const languageLinks = (locale: Locale): string =>
  SEO_LOCALES.map((other) => {
    const label = SEO_PAGES[other].label;
    const current = other === locale ? ' aria-current="page"' : '';

    return `<a href="${toRoot(locale)}${SEO_PAGES[other].folder}${ABOUT_FOLDER}" hreflang="${SEO_PAGES[other].htmlLang}"${current}>${label}</a>`;
  }).join(' · ');

/** The about page of one language: plain HTML that opens without the app. */
export const aboutHtml = (locale: Locale, lessonTitles: string[]): string => {
  const page = SEO_PAGES[locale];
  const copy = ABOUT_PAGES[locale];
  const title = escapeHtml(copy.title);
  const description = escapeHtml(copy.description);
  const list = (items: string[]): string => items.map((item) => `<li>${escapeHtml(item)}</li>`).join('\n          ');
  const questions = copy.questions
    .map(({ question, answer }) => `<dt>${escapeHtml(question)}</dt>\n          <dd>${escapeHtml(answer)}</dd>`)
    .join('\n          ');

  return `<!doctype html>
<html lang="${page.htmlLang}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>${title}</title>
    <meta name="description" content="${description}" />
    <link rel="icon" type="image/png" href="${toRoot(locale)}icone.png" />
    <link rel="canonical" href="${aboutUrl(locale)}" />
    ${alternateLinks()}
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Safira" />
    <meta property="og:url" content="${aboutUrl(locale)}" />
    <meta property="og:title" content="${title}" />
    <meta property="og:description" content="${description}" />
    <meta property="og:image" content="${SITE_URL}og/${locale}.jpg" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:locale" content="${page.ogLocale}" />
    <meta name="twitter:card" content="summary_large_image" />
    <style>${STYLE}    </style>
  </head>
  <body>
    <main>
      <header>
        <a class="brand" href="../"><img src="${toRoot(locale)}icone.png" alt="" width="40" height="40" />Safira</a>
        <a class="open" href="../">${escapeHtml(copy.openIde)}</a>
      </header>

      <h1>${escapeHtml(copy.heading)}</h1>
      <p class="lead">${escapeHtml(copy.lead)}</p>

      <section aria-labelledby="who">
        <h2 id="who">${escapeHtml(copy.whoTitle)}</h2>
        <ul>
          ${list(copy.who)}
        </ul>
      </section>

      <section aria-labelledby="example">
        <h2 id="example">${escapeHtml(copy.exampleTitle)}</h2>
        <p>${escapeHtml(copy.exampleText)}</p>
        <pre><code>${escapeHtml(copy.example)}</code></pre>
        <p class="label">${escapeHtml(copy.outputLabel)}</p>
        <pre><samp>${escapeHtml(copy.output.join('\n'))}</samp></pre>
      </section>

      <section aria-labelledby="lessons">
        <h2 id="lessons">${escapeHtml(copy.lessonsTitle)}</h2>
        <p>${escapeHtml(copy.lessonsText)}</p>
        <ol>
          ${list(lessonTitles)}
        </ol>
      </section>

      <section aria-labelledby="questions">
        <h2 id="questions">${escapeHtml(copy.questionsTitle)}</h2>
        <dl>
          ${questions}
        </dl>
      </section>

      <section aria-labelledby="history">
        <h2 id="history">${escapeHtml(copy.historyTitle)}</h2>
        <p>${escapeHtml(copy.history)}</p>
      </section>

      <section aria-labelledby="links">
        <h2 id="links">${escapeHtml(copy.linksTitle)}</h2>
        <ul>
          <li><a href="${REPOSITORY_URL}/wiki">${escapeHtml(copy.wiki)}</a></li>
          <li><a href="${REPOSITORY_URL}">${escapeHtml(copy.github)}</a></li>
          <li><a href="${REPOSITORY_URL}/blob/main/CHANGELOG.md">${escapeHtml(copy.changelog)}</a></li>
          <li><a href="${REPOSITORY_URL}/issues">${escapeHtml(copy.bug)}</a></li>
        </ul>
      </section>

      <footer>
        <nav aria-label="${escapeHtml(copy.languagesLabel)}">${languageLinks(locale)}</nav>
      </footer>
    </main>
  </body>
</html>
`;
};

/** The about pages go in the sitemap beside the app pages, each one pointing to the others. */
export const aboutSitemapUrls = (): string[] => {
  const alternates = SEO_LOCALES.map(
    (locale) =>
      `    <xhtml:link rel="alternate" hreflang="${SEO_PAGES[locale].htmlLang}" href="${aboutUrl(locale)}" />`,
  ).join('\n');

  return SEO_LOCALES.map((locale) => `  <url>\n    <loc>${aboutUrl(locale)}</loc>\n${alternates}\n  </url>`);
};
