// @ts-check

import starlight from "@astrojs/starlight";
import { defineConfig } from "astro/config";
import starlightThemeRapidePlugin from "starlight-theme-rapide";


export default defineConfig({
	site: "https://mdsreq-fga-unb.github.io",
	base: "/REQ-2025.2-T01-Softex",
	integrations: [
		starlight({
			plugins: [starlightThemeRapidePlugin()],
			title: "Softex - Sistema de Gestão de Recursos",
			social: [
				{
					icon: "github",
					label: "GitHub",
					href: "https://github.com/mdsreq-fga-unb/REQ-2025.2-T01-Softex",
				},
			],
			customCss: ['./src/styles/custom.css'],
			sidebar: [
				{
					label: "Início",
					items: [
						{
							label: "Sobre o Projeto",
							slug: "home/sobre",
						},
						{
							label: "Equipe",
							slug: "home/equipe",
						},
					],
				},
				{
					label: "Sistema",
					items: [
						{
							label: "Visão Geral",
							slug: "sistema/visao-geral",
						},
						{
							label: "Funcionalidades",
							slug: "sistema/funcionalidades",
						},
					],
				},
				{
					label: "Guia",
					items: [
						{
							label: "Instalação",
							slug: "guia/instalacao",
						},
						{
							label: "Uso",
							slug: "guia/uso",
						},
					],
				}
				
			],
		}),
	],
});
