import type { Locale } from '../language/messages.ts';
import { SEO_LOCALES, SEO_PAGES, SITE_URL } from './seoPages.ts';

export const ABOUT_FOLDER = 'about/';

const REPOSITORY_URL = 'https://github.com/gabrielogregorio/safira';

/** A piece of what a program shows, with the color it asked for. */
export interface ShownText {
  text: string;
  color?: string;
}

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
  output: ShownText[][];
  lessonsTitle: string;
  lessonsText: string;
  questionsTitle: string;
  questions: Question[];
  historyTitle: string;
  history: string[];
  contributeTitle: string;
  contributeText: string;
  idea: string;
  code: string;
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
    lead: 'Safira is a programming language in plain words, made for people who have never programmed. It works in English, Portuguese, Spanish, Chinese and Japanese, and you can even mix them in the same program. It runs right in the browser, on a computer or on a phone: nothing to install, no account and no ads.',
    openIde: 'Open the IDE',
    whoTitle: 'Who it is for',
    who: [
      'Anyone writing a first line of code, at any age.',
      'Teachers who want a first class on logic without installing anything.',
      'People who do not read English: Safira also speaks Portuguese, Spanish, Chinese and Japanese.',
    ],
    exampleTitle: 'A short program',
    exampleText: 'Many ways to show a text, the same line, two languages mixed, a loop and a condition:',
    outputLabel: 'What it shows',
    example:
      '# Many ways to say the same thing, with color.\nname receives "Ana"\nage is worth 12\nshow "Hello, " + name + "!" in color blue\ndisplay on the screen "You are " + age + " years old."\nwrite on the screen "All of these show a text." in color green\n\n# On the same line, and even in Portuguese.\nshow on this line "Safira "\nprint "speaks "\nmostre "Portuguese too."\n\nrepeat 3 times {\n    show on this line "⭐" in color yellow\n}\nshow ""\n\nif age is greater than or equal to 10 then {\n    show "You can code already! 🎉" in color pink\n} else {\n    show "You can too, with help! 🎉"\n}',
    output: [
      [{ text: 'Hello, Ana!', color: '#4da3ff' }],
      [{ text: 'You are 12 years old.' }],
      [{ text: 'All of these show a text.', color: '#35d07f' }],
      [{ text: 'Safira ' }, { text: 'speaks ' }, { text: 'Portuguese too.' }],
      [
        { text: '⭐', color: '#ffe14d' },
        { text: '⭐', color: '#ffe14d' },
        { text: '⭐', color: '#ffe14d' },
      ],
      [{ text: 'You can code already! 🎉', color: '#ff7ac6' }],
    ],
    lessonsTitle: 'The 14 lessons',
    lessonsText:
      'Open a project and choose Lesson mode in the Help menu. Each lesson shows a program to run and then a challenge, which Safira checks by itself.',
    questionsTitle: 'Questions',
    questions: [
      { question: 'Is it free?', answer: 'Yes. Safira is open source, under the MIT license.' },
      { question: 'Are there ads?', answer: 'No. There are no ads and nothing tracks what you do.' },
      {
        question: 'Can I change Safira or make my own version?',
        answer:
          'Yes. The code is on GitHub under the MIT license: you can copy it, change it and publish your own version, as long as you keep the license notice.',
      },
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
    history: [
      'Safira was born in August 2019, early in the career of Gabriel Gregorio, with one goal: letting people who had never programmed write their first program with the words they already use every day. The first version was a language and an IDE written in Python, installed on the computer, in Portuguese, English and Spanish.',
      'Version 0.38, from May 2021, was the last one in Python. In 2026 Safira was rewritten from scratch for the web, in TypeScript: version 1.0.0 took the IDE to the browser and to phones, added Chinese and Japanese, projects with folders, breakpoints, a variables inspector and the lessons with the cat. Now the first line of code is one link away.',
      'Before the Python code left the project, the output of its programs was recorded, and that recording became a test that still runs: scripts written for the Python version run the same on the web.',
    ],
    contributeTitle: 'Help build Safira',
    contributeText:
      'Safira is made in the open, on GitHub. Anyone can help: with an idea, a bug report, a translation fix or code.',
    idea: 'Suggest an idea',
    code: 'Contribute code: how to start',
    linksTitle: 'Learn more',
    wiki: 'Wiki: guide, commands and ready examples',
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
    lead: 'A Safira é uma linguagem de programação em português, feita para quem nunca programou. Ela também existe em inglês, espanhol, chinês e japonês, e dá para misturar os idiomas no mesmo programa. Roda direto no navegador, no computador ou no celular: sem instalar nada, sem conta e sem anúncios.',
    openIde: 'Abrir a IDE',
    whoTitle: 'Para quem é',
    who: [
      'Quem vai escrever a primeira linha de código, em qualquer idade.',
      'Professores que querem uma primeira aula de lógica sem instalar nada.',
      'Quem não lê inglês: a Safira fala português, e também inglês, espanhol, chinês e japonês.',
    ],
    exampleTitle: 'Um programa curto',
    exampleText:
      'Várias formas de mostrar um texto, a mesma linha, dois idiomas misturados, uma repetição e uma condição:',
    outputLabel: 'O que ele mostra',
    example:
      '# Várias formas de dizer a mesma coisa, com cor.\nnome recebe "Ana"\nidade vale 12\nmostre "Olá, " + nome + "!" na cor azul\nexiba "Você tem " + idade + " anos."\nimprima na tela "Tudo isso mostra um texto." na cor verde\n\n# Na mesma linha, e até em inglês.\nmostre nessa linha "A Safira "\nprint "fala "\nshow "inglês também."\n\nrepita 3 vezes {\n    mostre nessa linha "⭐" na cor amarelo\n}\nmostre ""\n\nse idade for maior ou igual a 10 então {\n    mostre "Já dá para programar! 🎉" na cor rosa\n} senão {\n    mostre "Dá também, com ajuda! 🎉"\n}',
    output: [
      [{ text: 'Olá, Ana!', color: '#4da3ff' }],
      [{ text: 'Você tem 12 anos.' }],
      [{ text: 'Tudo isso mostra um texto.', color: '#35d07f' }],
      [{ text: 'A Safira ' }, { text: 'fala ' }, { text: 'inglês também.' }],
      [
        { text: '⭐', color: '#ffe14d' },
        { text: '⭐', color: '#ffe14d' },
        { text: '⭐', color: '#ffe14d' },
      ],
      [{ text: 'Já dá para programar! 🎉', color: '#ff7ac6' }],
    ],
    lessonsTitle: 'As 14 aulas',
    lessonsText:
      'Abra um projeto e escolha Modo aula no menu Ajuda. Cada aula mostra um programa para rodar e depois um desafio, que a Safira confere sozinha.',
    questionsTitle: 'Dúvidas',
    questions: [
      { question: 'É grátis?', answer: 'Sim. A Safira é de código aberto, com licença MIT.' },
      { question: 'Tem anúncio?', answer: 'Não. Não tem anúncio e nada rastreia o que você faz.' },
      {
        question: 'Posso modificar a Safira ou criar a minha versão?',
        answer:
          'Pode. O código está no GitHub com licença MIT: você pode copiar, modificar e publicar a sua versão, desde que mantenha o aviso da licença.',
      },
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
    history: [
      'A Safira nasceu em agosto de 2019, no começo da carreira de Gabriel Gregorio, com um objetivo: deixar quem nunca programou escrever o primeiro programa com as palavras que já usa no dia a dia. A primeira versão era uma linguagem e uma IDE feitas em Python, instaladas no computador, em português, inglês e espanhol.',
      'A versão 0.38, de maio de 2021, foi a última em Python. Em 2026 a Safira foi reescrita do zero para a web, em TypeScript: a versão 1.0.0 levou a IDE para o navegador e para o celular, trouxe chinês e japonês, projetos com pastas, pontos de parada, inspetor de variáveis e as aulas com o gato. Agora a primeira linha de código está a um link de distância.',
      'Antes de o código em Python sair do projeto, a saída dos programas foi gravada, e essa gravação virou um teste que roda até hoje: os scripts feitos para a versão em Python rodam igual na web.',
    ],
    contributeTitle: 'Ajude a construir a Safira',
    contributeText:
      'A Safira é feita às claras, no GitHub. Qualquer pessoa pode ajudar: com uma ideia, um problema encontrado, uma correção de tradução ou código.',
    idea: 'Sugerir uma ideia',
    code: 'Contribuir com código: por onde começar',
    linksTitle: 'Saiba mais',
    wiki: 'Wiki: guia, comandos e exemplos prontos',
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
    lead: 'Safira es un lenguaje de programación en español, hecho para quien nunca programó. También existe en inglés, portugués, chino y japonés, y se pueden mezclar los idiomas en el mismo programa. Funciona directo en el navegador, en el ordenador o en el móvil: sin instalar nada, sin cuenta y sin anuncios.',
    openIde: 'Abrir el IDE',
    whoTitle: 'Para quién es',
    who: [
      'Quien va a escribir su primera línea de código, a cualquier edad.',
      'Docentes que quieren una primera clase de lógica sin instalar nada.',
      'Quien no lee inglés: Safira habla español, y también portugués, inglés, chino y japonés.',
    ],
    exampleTitle: 'Un programa corto',
    exampleText:
      'Varias formas de mostrar un texto, la misma línea, dos idiomas mezclados, una repetición y una condición:',
    outputLabel: 'Lo que muestra',
    example:
      '# Muchas formas de decir lo mismo, con color.\nnombre recibe "Ana"\nedad vale 12\nmuestra "¡Hola, " + nombre + "!" en color azul\nimprimir en la pantalla "Tienes " + edad + " años."\nescribe en la pantalla "Todo esto muestra un texto." en color verde\n\n# En la misma línea, y hasta en inglés.\nmostrar en esta linea "Safira "\nprint "habla "\nshow "inglés también."\n\nrepetir 3 veces {\n    mostrar en esta linea "⭐" en color amarillo\n}\nmuestra ""\n\nsi edad es mayor o igual a 10 entonces {\n    muestra "¡Ya puedes programar! 🎉" en color rosa\n} si no {\n    muestra "¡También puedes, con ayuda! 🎉"\n}',
    output: [
      [{ text: '¡Hola, Ana!', color: '#4da3ff' }],
      [{ text: 'Tienes 12 años.' }],
      [{ text: 'Todo esto muestra un texto.', color: '#35d07f' }],
      [{ text: 'Safira ' }, { text: 'habla ' }, { text: 'inglés también.' }],
      [
        { text: '⭐', color: '#ffe14d' },
        { text: '⭐', color: '#ffe14d' },
        { text: '⭐', color: '#ffe14d' },
      ],
      [{ text: '¡Ya puedes programar! 🎉', color: '#ff7ac6' }],
    ],
    lessonsTitle: 'Las 14 lecciones',
    lessonsText:
      'Abre un proyecto y elige Modo clase en el menú Ayuda. Cada lección muestra un programa para ejecutar y después un desafío, que Safira revisa sola.',
    questionsTitle: 'Dudas',
    questions: [
      { question: '¿Es gratis?', answer: 'Sí. Safira es de código abierto, con licencia MIT.' },
      { question: '¿Tiene anuncios?', answer: 'No. No hay anuncios y nada rastrea lo que haces.' },
      {
        question: '¿Puedo modificar Safira o crear mi propia versión?',
        answer:
          'Sí. El código está en GitHub con licencia MIT: puedes copiarlo, modificarlo y publicar tu propia versión, siempre que mantengas el aviso de la licencia.',
      },
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
    history: [
      'Safira nació en agosto de 2019, al comienzo de la carrera de Gabriel Gregorio, con un objetivo: que quien nunca programó pudiera escribir su primer programa con las palabras que ya usa todos los días. La primera versión era un lenguaje y un IDE hechos en Python, instalados en el ordenador, en portugués, inglés y español.',
      'La versión 0.38, de mayo de 2021, fue la última en Python. En 2026 Safira fue reescrita desde cero para la web, en TypeScript: la versión 1.0.0 llevó el IDE al navegador y al móvil, sumó chino y japonés, proyectos con carpetas, puntos de parada, inspector de variables y las lecciones con el gato. Ahora la primera línea de código está a un enlace.',
      'Antes de que el código en Python saliera del proyecto, se grabó la salida de sus programas, y esa grabación se convirtió en una prueba que sigue funcionando: los scripts hechos para la versión en Python funcionan igual en la web.',
    ],
    contributeTitle: 'Ayuda a construir Safira',
    contributeText:
      'Safira se hace a la vista de todos, en GitHub. Cualquiera puede ayudar: con una idea, un problema encontrado, una corrección de traducción o código.',
    idea: 'Sugerir una idea',
    code: 'Contribuir con código: por dónde empezar',
    linksTitle: 'Saber más',
    wiki: 'Wiki: guía, comandos y ejemplos listos',
    github: 'Código en GitHub',
    changelog: 'Qué cambió en cada versión',
    bug: 'Reportar un problema',
    languagesLabel: 'Idiomas',
  },
  'zh-cn': {
    title: '关于 Safira：用中文学编程，免费，直接在浏览器中运行',
    description: 'Safira 是什么、适合谁、一个小程序、14 节课程、常见问题解答，以及维基和源代码的链接。',
    heading: '关于 Safira',
    lead: 'Safira 是一门可以用中文书写的编程语言，专为从没写过代码的人设计。它同样支持英语、葡萄牙语、西班牙语和日语，同一个程序里还能混用多种语言。程序直接在浏览器里运行，电脑和手机都可以：无需安装，无需注册，没有广告。',
    openIde: '打开 IDE',
    whoTitle: '适合谁',
    who: [
      '任何年龄、准备写下第一行代码的人。',
      '想在不安装任何软件的情况下上第一堂逻辑课的老师。',
      '不懂英语的人：Safira 会说中文，也会说英语、葡萄牙语、西班牙语和日语。',
    ],
    exampleTitle: '一个小程序',
    exampleText: '多种显示文字的写法、同一行输出、混用两种语言、一次重复和一个条件：',
    outputLabel: '运行结果',
    example:
      '# 同一件事，有很多种说法，还能加颜色。\n名字 设为 "小明"\n年龄 赋值 12\n显示 "你好，" + 名字 + "！" 颜色 蓝色\n打印 "你今年 " + 年龄 + " 岁。"\n输出 "这些都能显示文字。" 颜色 绿色\n\n# 写在同一行，甚至可以用英语。\n同行显示 "Safira "\n同行打印 "也会说"\nshow "英语。"\n\n重复 3 次 {\n    同行显示 "⭐" 颜色 黄色\n}\n显示 ""\n\n如果 年龄 大于等于 10 那么 {\n    显示 "你已经可以编程了！🎉" 颜色 粉色\n} 否则 {\n    显示 "有人帮忙也可以！🎉"\n}',
    output: [
      [{ text: '你好，小明！', color: '#4da3ff' }],
      [{ text: '你今年 12 岁。' }],
      [{ text: '这些都能显示文字。', color: '#35d07f' }],
      [{ text: 'Safira ' }, { text: '也会说' }, { text: '英语。' }],
      [
        { text: '⭐', color: '#ffe14d' },
        { text: '⭐', color: '#ffe14d' },
        { text: '⭐', color: '#ffe14d' },
      ],
      [{ text: '你已经可以编程了！🎉', color: '#ff7ac6' }],
    ],
    lessonsTitle: '14 节课程',
    lessonsText:
      '打开一个项目，在「帮助」菜单中选择「课程模式」。每节课先给出一个可以运行的程序，然后是一个挑战，Safira 会自动检查你的答案。',
    questionsTitle: '常见问题',
    questions: [
      { question: '免费吗？', answer: '免费。Safira 是开源软件，采用 MIT 许可证。' },
      { question: '有广告吗？', answer: '没有。没有广告，也不会追踪你的操作。' },
      {
        question: '我可以修改 Safira 或做自己的版本吗？',
        answer: '可以。源代码在 GitHub 上，采用 MIT 许可证：你可以复制、修改并发布自己的版本，只需保留许可证声明。',
      },
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
    history: [
      'Safira 诞生于 2019 年 8 月，那时 Gabriel Gregorio 刚开始职业生涯。它的目标只有一个：让从没写过代码的人，用日常说话的词语写出第一个程序。第一个版本是用 Python 编写、安装在电脑上的语言和 IDE，支持葡萄牙语、英语和西班牙语。',
      '2021 年 5 月发布的 0.38 是最后一个 Python 版本。2026 年，Safira 用 TypeScript 为网页从头重写：1.0.0 版本把 IDE 带进了浏览器和手机，新增了中文和日语、带文件夹的项目、断点、变量查看器，以及由小猫带领的课程。现在，打开一个链接就能写下第一行代码。',
      '在 Python 代码移出项目之前，所有程序的输出都被记录了下来，这份记录变成了一项至今仍在运行的测试：为 Python 版本写的脚本，在网页版上运行结果完全一样。',
    ],
    contributeTitle: '一起建设 Safira',
    contributeText: 'Safira 在 GitHub 上公开开发。任何人都可以帮忙：提一个想法、报告一个问题、修正翻译或贡献代码。',
    idea: '提出想法',
    code: '贡献代码：从哪里开始',
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
    lead: 'Safira は日本語で書けるプログラミング言語で、プログラミングをしたことがない人のために作られました。英語、ポルトガル語、スペイン語、中国語にも対応していて、同じプログラムの中で言語を混ぜることもできます。ブラウザでそのまま動き、パソコンでもスマホでも使えます。インストールも登録も不要で、広告もありません。',
    openIde: 'IDE を開く',
    whoTitle: '誰のためのもの',
    who: [
      '年齢を問わず、はじめてコードを書く人。',
      '何もインストールせずに、論理の最初の授業をしたい先生。',
      '英語が読めない人：Safira は日本語のほか、英語、ポルトガル語、スペイン語、中国語も話します。',
    ],
    exampleTitle: '短いプログラム',
    exampleText: '文字を表示するいろいろな書き方、同じ行への表示、2 つの言語の混在、くり返し、条件：',
    outputLabel: '表示される結果',
    example:
      '# 同じことを、いろいろな言い方で。色も付けられます。\n名前 は "さくら"\n年齢 は 12\n表示 "こんにちは、" + 名前 + "！" 色 青\n出力 "あなたは " + 年齢 + " 歳です。"\n表示 "どれも文字を表示します。" 色 緑\n\n# 同じ行に、英語でも。\n続けて表示 "Safira は"\nprint "英語も"\nshow "話せます。"\n\n繰り返す 3 回 {\n    続けて表示 "⭐" 色 黄色い\n}\n表示 ""\n\nもし 年齢 以上 10 なら {\n    表示 "もうプログラミングできます! 🎉" 色 ピンク\n} そうでなければ {\n    表示 "手伝ってもらえばできます! 🎉"\n}',
    output: [
      [{ text: 'こんにちは、さくら！', color: '#4da3ff' }],
      [{ text: 'あなたは 12 歳です。' }],
      [{ text: 'どれも文字を表示します。', color: '#35d07f' }],
      [{ text: 'Safira は' }, { text: '英語も' }, { text: '話せます。' }],
      [
        { text: '⭐', color: '#ffe14d' },
        { text: '⭐', color: '#ffe14d' },
        { text: '⭐', color: '#ffe14d' },
      ],
      [{ text: 'もうプログラミングできます! 🎉', color: '#ff7ac6' }],
    ],
    lessonsTitle: '14 のレッスン',
    lessonsText:
      'プロジェクトを開いて、「ヘルプ」メニューから「レッスンモード」を選びます。各レッスンでは、まず動かすプログラムがあり、次にチャレンジがあります。答えは Safira が自動でチェックします。',
    questionsTitle: 'よくある質問',
    questions: [
      { question: '無料ですか？', answer: 'はい。Safira はオープンソースで、MIT ライセンスです。' },
      { question: '広告はありますか？', answer: 'いいえ。広告はなく、操作を追跡するものもありません。' },
      {
        question: 'Safira を改造したり、自分のバージョンを作ったりできますか？',
        answer:
          'はい。ソースコードは GitHub にあり、MIT ライセンスです。ライセンス表示を残せば、コピーして改造し、自分のバージョンを公開できます。',
      },
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
    history: [
      'Safira は 2019 年 8 月、Gabriel Gregorio のキャリアの初期に生まれました。目標はひとつ、プログラミングをしたことがない人が、ふだん使っている言葉で最初のプログラムを書けるようにすることです。最初のバージョンは Python で作られ、パソコンにインストールする言語と IDE で、ポルトガル語、英語、スペイン語に対応していました。',
      '2021 年 5 月の 0.38 が最後の Python 版です。2026 年、Safira は TypeScript でウェブ向けに一から書き直されました。バージョン 1.0.0 で IDE がブラウザとスマホに移り、中国語と日本語、フォルダ付きのプロジェクト、ブレークポイント、変数インスペクター、猫と学ぶレッスンが加わりました。今ではリンクひとつで最初の一行が書けます。',
      'Python のコードがプロジェクトから外れる前に、プログラムの出力がすべて記録され、その記録は今も動くテストになりました。Python 版のために書いたスクリプトは、ウェブでも同じように動きます。',
    ],
    contributeTitle: 'Safira づくりに参加する',
    contributeText:
      'Safira は GitHub で公開して作られています。アイデア、見つけた問題、翻訳の修正、コードなど、誰でも手伝えます。',
    idea: 'アイデアを提案する',
    code: 'コードで貢献する：はじめかた',
    linksTitle: 'もっと知る',
    wiki: 'ウィキ：ガイド、命令、使用例',
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

// The same Frutiger Aero as the app: sky and hills behind, glass panels, glossy pill buttons and a dark terminal.
const STYLE = `
      :root {
        --ink: #0b2a4a;
        --sky-color: #7fd1f7;
        --muted: #234a6e;
        --link: #0d4fae;
        --panel: rgb(255 255 255 / 62%);
        --border: rgb(255 255 255 / 85%);
        --shadow: 0 8px 28px rgb(6 50 100 / 28%), inset 0 1px 0 rgb(255 255 255 / 85%);
        --editor: linear-gradient(180deg, rgb(255 255 255 / 92%), rgb(232 245 255 / 88%));
        --sky:
          radial-gradient(circle at 12% 22%, rgb(255 255 255 / 55%) 0 2.2vmin, transparent 2.4vmin),
          radial-gradient(circle at 86% 38%, rgb(255 255 255 / 55%) 0 1.2vmin, transparent 1.4vmin),
          radial-gradient(circle at 70% 12%, rgb(255 255 255 / 45%) 0 1vmin, transparent 1.2vmin),
          radial-gradient(90vmax 26vmax at 22% 118%, #9be86a 0 70%, transparent 71%),
          radial-gradient(110vmax 24vmax at 82% 124%, #55c93b 0 70%, transparent 71%),
          linear-gradient(180deg, #2f9fe8 0%, #7fd1f7 42%, #d6f4ff 72%, #eefcff 100%);
        color-scheme: light;
      }

      @media (prefers-color-scheme: dark) {
        :root {
          --ink: #eaf6ff;
          --sky-color: #082f5c;
          --muted: #b9daf2;
          --link: #8fd0ff;
          --panel: rgb(8 32 66 / 66%);
          --border: rgb(150 225 255 / 35%);
          --shadow: 0 8px 28px rgb(0 0 0 / 45%), inset 0 1px 0 rgb(170 235 255 / 28%);
          --editor: linear-gradient(180deg, rgb(14 44 84 / 92%), rgb(8 30 60 / 92%));
          --sky:
            radial-gradient(70vmax 22vmax at 40% 30%, rgb(90 255 200 / 26%), transparent 70%),
            radial-gradient(circle at 12% 12%, #ffffff 0 1px, transparent 2px),
            radial-gradient(circle at 34% 22%, #ffffff 0 1px, transparent 2px),
            radial-gradient(circle at 62% 8%, #ffffff 0 1px, transparent 2px),
            radial-gradient(circle at 88% 18%, #ffffff 0 1px, transparent 2px),
            radial-gradient(90vmax 26vmax at 22% 118%, #0b6e5c 0 70%, transparent 71%),
            radial-gradient(110vmax 24vmax at 82% 124%, #074c44 0 70%, transparent 71%),
            linear-gradient(180deg, #04142f 0%, #082f5c 48%, #0a5a6a 82%, #0f8a6d 100%);
          color-scheme: dark;
        }
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        background: var(--sky-color);
        color: var(--ink);
        font-family: system-ui, sans-serif;
        line-height: 1.6;
        min-height: 100vh;
      }

      /* A layer of its own, because phones ignore a fixed background: the hills stay at the bottom of the screen. */
      body::before {
        position: fixed;
        z-index: -1;
        inset: 0;
        background: var(--sky);
        content: '';
      }

      main {
        max-width: 780px;
        margin: 0 auto;
        padding: 20px 16px 48px;
      }

      .glass {
        backdrop-filter: blur(14px) saturate(150%);
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 16px;
        box-shadow: var(--shadow);
      }

      header {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        align-items: center;
        justify-content: space-between;
        padding: 10px 12px 10px 16px;
        border-radius: 999px;
      }

      .brand {
        display: flex;
        gap: 10px;
        align-items: center;
        color: inherit;
        font-weight: 700;
        font-size: 1.25rem;
        text-decoration: none;
      }

      .brand img {
        border-radius: 50%;
        box-shadow: 0 2px 8px rgb(6 50 100 / 30%);
      }

      .open {
        display: inline-block;
        padding: 9px 20px;
        border: 1px solid #3fa52a;
        border-radius: 999px;
        background: linear-gradient(180deg, #e4ffd0 0%, #a8f07a 48%, #6fdc45 52%, #b4f58c 100%);
        box-shadow:
          0 2px 5px rgb(6 50 100 / 28%),
          inset 0 1px 0 rgb(255 255 255 / 95%);
        color: #07330b;
        font-weight: 700;
        text-decoration: none;
        transition:
          filter 120ms ease,
          transform 120ms ease;
      }

      .open:hover {
        filter: brightness(1.05) saturate(1.2);
        transform: translateY(-1px);
      }

      .hero {
        margin-top: 20px;
        padding: 8px 24px 20px;
      }

      h1 {
        margin: 16px 0 8px;
        font-size: 2.1rem;
        line-height: 1.2;
      }

      .lead {
        margin: 0;
        color: var(--muted);
        font-size: 1.1rem;
      }

      section {
        margin-top: 20px;
        padding: 4px 24px 18px;
      }

      h2 {
        margin: 20px 0 12px;
        font-size: 1.3rem;
      }

      pre {
        overflow-x: auto;
        margin: 0;
        padding: 16px;
        border-radius: 12px;
        font-size: 0.95rem;
      }

      .editor {
        background: var(--editor);
        border: 1px solid var(--border);
        box-shadow: inset 0 1px 3px rgb(6 50 100 / 18%);
      }

      .terminal {
        background: linear-gradient(180deg, #0c2340 0%, #050f20 100%);
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        color: #dff4ff;
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

        .hero,
        section {
          padding-right: 16px;
          padding-left: 16px;
        }
      }

      dt {
        margin-top: 16px;
        font-weight: 700;
      }

      dd {
        margin: 4px 0 0;
        color: var(--muted);
      }

      a {
        color: var(--link);
      }

      footer {
        margin-top: 28px;
        padding: 12px 16px;
        border-radius: 999px;
        font-size: 0.95rem;
        text-align: center;
      }
`;

// The colors come from the program and are always a hex color, as the language resolves them.
const shownLine = (pieces: ShownText[]): string =>
  pieces
    .map(({ text, color }) =>
      color === undefined ? escapeHtml(text) : `<span style="color: ${color}">${escapeHtml(text)}</span>`,
    )
    .join('');

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
      <header class="glass">
        <a class="brand" href="../"><img src="${toRoot(locale)}icone.png" alt="" width="40" height="40" />Safira</a>
        <a class="open" href="../">${escapeHtml(copy.openIde)}</a>
      </header>

      <div class="hero glass">
        <h1>${escapeHtml(copy.heading)}</h1>
        <p class="lead">${escapeHtml(copy.lead)}</p>
      </div>

      <section class="glass" aria-labelledby="who">
        <h2 id="who">${escapeHtml(copy.whoTitle)}</h2>
        <ul>
          ${list(copy.who)}
        </ul>
      </section>

      <section class="glass" aria-labelledby="example">
        <h2 id="example">${escapeHtml(copy.exampleTitle)}</h2>
        <p>${escapeHtml(copy.exampleText)}</p>
        <pre class="editor"><code>${escapeHtml(copy.example)}</code></pre>
        <p class="label">${escapeHtml(copy.outputLabel)}</p>
        <pre class="terminal"><samp>${copy.output.map(shownLine).join('\n')}</samp></pre>
      </section>

      <section class="glass" aria-labelledby="lessons">
        <h2 id="lessons">${escapeHtml(copy.lessonsTitle)}</h2>
        <p>${escapeHtml(copy.lessonsText)}</p>
        <ol>
          ${list(lessonTitles)}
        </ol>
      </section>

      <section class="glass" aria-labelledby="questions">
        <h2 id="questions">${escapeHtml(copy.questionsTitle)}</h2>
        <dl>
          ${questions}
        </dl>
      </section>

      <section class="glass" aria-labelledby="history">
        <h2 id="history">${escapeHtml(copy.historyTitle)}</h2>
        ${copy.history.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join('\n        ')}
      </section>

      <section class="glass" aria-labelledby="contribute">
        <h2 id="contribute">${escapeHtml(copy.contributeTitle)}</h2>
        <p>${escapeHtml(copy.contributeText)}</p>
        <ul>
          <li><a href="${REPOSITORY_URL}/issues/new?template=feature_request.yml">${escapeHtml(copy.idea)}</a></li>
          <li><a href="${REPOSITORY_URL}/issues/new?template=bug_report.yml">${escapeHtml(copy.bug)}</a></li>
          <li><a href="${REPOSITORY_URL}/blob/main/CONTRIBUTING.md">${escapeHtml(copy.code)}</a></li>
        </ul>
      </section>

      <section class="glass" aria-labelledby="links">
        <h2 id="links">${escapeHtml(copy.linksTitle)}</h2>
        <ul>
          <li><a href="${REPOSITORY_URL}/wiki">${escapeHtml(copy.wiki)}</a></li>
          <li><a href="${REPOSITORY_URL}">${escapeHtml(copy.github)}</a></li>
          <li><a href="${REPOSITORY_URL}/blob/main/CHANGELOG.md">${escapeHtml(copy.changelog)}</a></li>
        </ul>
      </section>

      <footer class="glass">
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
