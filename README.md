# Frezza Voice Studio

Derivação independente do [VoiceStudio v0.5.6](https://github.com/debpalash/VoiceStudio/tree/v0.5.6), originalmente desenvolvido por Palash Debnath e colaboradores.

## Status
Este repositório inicia com uma rotina de **importação do código-fonte oficial** e uma rotina de **compilação Windows x64**. A importação copia a árvore correspondente à tag `v0.5.6`, preserva a licença AGPL-3.0 e aplica uma identidade de build independente. Não contém, nem afirma desbloquear, funcionalidades proprietárias ausentes do fonte público.

## Como usar
1. Abra **Actions → 01 - Importar fonte v0.5.6 → Run workflow**.
2. Quando a importação terminar, abra **Actions → 02 - Gerar Windows EXE → Run workflow**.
3. Baixe o instalador em **Artifacts** na execução de build.

O segundo workflow só funciona após a importação. A primeira inicialização do aplicativo pode baixar Python, bibliotecas e pesos de modelos, conforme o projeto original.

## Diferenças da compilação Frezza
- Nome de produto e identificador de aplicação próprios.
- Instalador Windows x64 gerado a partir do código-fonte, sem modificar o executável original.
- Canal de atualização do projeto original desativado nesta compilação (sem apontar para URLs do mantenedor).
- Construção reproduzível baseada na tag fixa `v0.5.6`.
- Os fluxos locais abertos são mantidos, com seus limites de estabilidade e requisitos normais de modelo/hardware.

## Licença
O aplicativo derivado permanece sob **AGPL-3.0-only**. Os avisos originais, o arquivo `LICENSE` e licenças de componentes permanecem. Pesos/modelos têm licenças independentes. O padrão `k2-fsa/OmniVoice` traz restrição não comercial sobre os pesos; este repositório não concede direitos adicionais.

Não confundir ausência de assinatura do instalador com ausência de licença: o Windows pode exibir SmartScreen para executáveis não assinados.
